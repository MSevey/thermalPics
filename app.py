# Web Server
from flask import Flask
from flask import request, redirect, render_template, url_for
# Database
from flask_sqlalchemy import SQLAlchemy
# images
from PIL import Image
import os
import numpy as np

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

    def __init__(self, name, maxTemp, minTemp, averageTemp):
        self.name = name
        self.maxTemp = maxTemp
        self.minTemp = minTemp
        self.averageTemp = averageTemp
        # self.latitude = latitude
        # self.longitude = longitude

    def __repr__(self):
        return "<ImageData %r>" % self.id


# function for reading tif and jpg images and returning temp data and GPS data
# stores information in database
#
# Current runtime is O(i*w*h) where i is # images, w and h are the width and height
#   in pixels for the tiff file.  If built in max, min, and mean are runtimes of O(n)
#   then the runtime would be O(i*(wh^2)) so it would be faster to calculate the max,
#   min, and average while looping over the pixels
def pixels(tifDir, jpgDir):
    # iT = Image.open(tifDir + 'DJI_0034.tif')
    # fnT, fextT = os.path.splitext(os.path.basename(tifDir + 'DJI_0034.tif'))

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
            exifData = iJ._getexif()

            # Find max and min temps, create empty array for temps
            temps = []
            # determining size of the tiff file
            size = w,h = iT.size
            # Loop over impage pixel by pixle
            for x in range(w):
                for y in range(h):
                    temps.append(iT.getpixel((x,y)))

            img = ImageData(fn, max(temps), min(temps), np.mean(temps))
            db.session.add(img)
            db.session.commit()

    # find GPS coordinates from jpg files
    # store files to database if doesn't exit

    return;


# setting root route
@app.route('/')
def index():
    imgs = ImageData.query.all()
    return render_template('index.html', imgs=imgs)

# setting img analysis route
@app.route('/post_imgs')
def post_imgs():
    pixels(tifDir, jpgDir)
    return redirect(url_for('index'))


# running main application
if __name__ == "__main__":
    app.run()
