# Web Server
from flask import Flask
from flask import request, redirect, render_template, url_for
# Database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# images
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import numpy as np
# env variables
import configvars

# initializing app and configuring
app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pguser:password@localhost/thermal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Setting global variables for directories
tifDir = './static/imagesRM/tif/'
jpgDir = './static/imagesRM/jpg/'

# creating imagedata model
class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    maxTemp = db.Column(db.Float)
    minTemp = db.Column(db.Float)
    averageTemp = db.Column(db.Float)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, name, maxTemp, minTemp, averageTemp, longitude, latitude):
        self.name = name
        self.maxTemp = maxTemp
        self.minTemp = minTemp
        self.averageTemp = averageTemp
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return "<ImageData %r>" % self.id


# function for reading tif and jpg images and returning temp data and GPS data
# stores information in database
#
# Current runtime is O(i*w*h) where i is # images, w and h are the width and height
#   in pixels for the tiff file.  If built in max, min, and mean are runtimes of O(n)
#   then the runtime would be O(i*(wh^2)) so it would be faster to calculate the max,
#   min, and average while looping over the pixels
def get_image_data(tifDir, jpgDir):
    # T denotes tif variable, J denotes jpg variable
    # Loop over tiff files
    for fT in os.listdir(tifDir):
        # verifying it is a TIFF file
        if fT.endswith('.tif'):
            # Opening image file and splitting file name and extension
            iT = Image.open(tifDir+fT)
            fn, fextT = os.path.splitext(fT)

            # Finding cooresponding jpg file
            fextJ = '.jpg'
            fJ = jpgDir + fn + fextJ
            iJ = Image.open(fJ)

            # Getting GPS coordinates
            exifData = get_exif_data(iJ)
            lat, lon = get_lat_lon(exifData)

            # Find max and min temps, create empty array for temps
            temps = []
            # determining size of the tiff file
            size = w,h = iT.size
            # Loop over impage pixel by pixle
            for x in range(w):
                for y in range(h):
                    temps.append(iT.getpixel((x,y)))


            # store image data to database
            img = ImageData(fn, max(temps), min(temps), np.mean(temps), lon, lat)
            db.session.add(img)
            db.session.commit()

    return;

# the follwing functions were referenced from https://gist.github.com/erans/983821
#   exifDataFunc(), _get_if_exist(), get_lat_lon(), get_lat_lon(), _convert_to_degress()
def get_exif_data(image):
    # Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None

def get_lat_lon(exif_data):
    # Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def _convert_to_degress(value):
    # Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

# querying images
imgs = ImageData.query.all()
overallMaxTemp = max(ImageData.query.with_entities(ImageData.maxTemp).all())
overallMinTemp = min(ImageData.query.with_entities(ImageData.minTemp).all())
overallAvgTemp = np.mean(ImageData.query.with_entities(ImageData.averageTemp).all())

# setting root route
# map of pointers
@app.route('/')
def index():
    return render_template('index.html', mapAPI=configvars.google_maps_API, imgs=imgs, avg=overallAvgTemp)

# setting hello route for React testing
@app.route('/hello')
def hello():
    return render_template('hello.html')

# setting route for displaying data
@app.route('/data')
def data():
    return render_template('data.html', imgs=imgs, max=overallMaxTemp, min=overallMinTemp, avg=overallAvgTemp)

# setting img analysis route
@app.route('/post_imgs')
def post_imgs():
    if imgs is None:
        get_image_data(tifDir, jpgDir)
    return redirect(url_for('data'))

# running main application
if __name__ == "__main__":
    app.run()
