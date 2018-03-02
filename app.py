# Web Server
from flask import Flask

# initializing app and configuring
app = Flask(__name__)
app.debug = True

# setting route route
@app.route('/')
def index():
    return 'raptor maps challenge'

# running main application
if __name__ == "__main__":
    app.run()
