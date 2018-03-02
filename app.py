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

# creating imagedata model
class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    maxTemp = db.Column(db.Float)
    minTemp = db.Column(db.Float)
    averageTemp = db.Column(db.Float)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, maxTemp, minTemp, averageTemp):
        self.name = name
        self.maxTemp = maxTemp
        self.minTemp = minTemp
        self.averageTemp = averageTemp
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "<ImageData %r>" % self.id

# OPTIMIZATIONS
# current function has run time of O(n^2), if avoid this scaling issue, in real application I would
#   do this analysis as images came in so the sample set was always small. Or
#   if possible pass in the two files at once instead of looping over a directory
def pixels():
    # T denotes tif variable, J denotes jpg variable
    # Loop over tiff files
    # for fT in os.listdir('./static/imagesRM/tif/'):
    #     # verifying it is a TIFF file
    #     if fT.endswith('.tif'):
    #         iT = Image.open(fT)
    iT = Image.open('./static/imagesRM/tif/DJI_0034.tif')
    # fnT, fextT = os.path.splitext(fT)
    fnT, fextT = os.path.splitext('./static/imagesRM/tif/DJI_0034.tif')
            # # Loop over jpg files to find cooresponding file
            # for fJ in os.listdir('./static/imagesRM/jpg/'):
            #     # verifying it is a jpg file
            #     if fJ.endswith('jpg'):
            #         fnJ, fextJ = os.path.splitext(fJ)
            #         if fnT == fnJ:
            #             iJ = Image.open(fJ)
            #             # assuming no duplicate image names
            #             break
        # Find max and min temps
    size = w,h = iT.size
    # Loop over impage pixel by pixle
    temps = []
    for x in range(w):
        for y in range(h):
            temps.append(iT.getpixel((x,y)))

    # find max, min, average temps from tiff files
    # find GPS coordinates from jpg files
    # store files to database if doesn't exit
    # pixel = i.getpixel(coordinate)
    # exifData = i._getexif()
    return max(temps), min(temps), np.mean(temps);

# pixels('./static/imagesRM/jpg/DJI_0034.jpg')

# for looping over images in current directory
# size_300 = (300,300)
# for f in os.listdir('.'):
#     # checks for files ending in .jpg
#     if f.endswith('.jpg'):
#         # opens file as an object i
#         i = Image.open(f)
#         # splitting fn (filename) and fext (file extension)
#         fn, fext = os.path.splitext(f)
#         # if i wanted to save them in a different format and folder or different size
#         i.thumbnail(size_300)
#         i.save('dir/{}{}'.format(fn,fext))



# setting route route
@app.route('/')
def index():
    imgs = ImageData.query.all()
    return render_template('index.html', imgs=imgs, function=pixels)


# running main application
if __name__ == "__main__":
    app.run()
