# Web Server
from flask import Flask
from flask import request, redirect, render_template, url_for
# Database
from flask_sqlalchemy import SQLAlchemy
# images
from PIL import Image

# initializing app and configuring
app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pguser:password@localhost/thermal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# creating image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxTemp = db.Column(db.Float)
    minTemp = db.Column(db.Float)
    averageTemp = db.Column(db.Float)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, maxTemp, minTemp, averageTemp):
        self.maxTemp = maxTemp
        self.minTemp = minTemp
        self.averageTemp = averageTemp
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "<Imagejpg %r>" % self.id


# setting route route
@app.route('/')
def index():
    images = Image.query.all()
    return render_template('index.html', Image=Image)


# running main application
if __name__ == "__main__":
    app.run()
