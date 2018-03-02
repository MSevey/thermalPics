# Thermal Picture Processor

This is a Python app using a Flask server.  It takes in jpg and tif thermal picture files
and determines min, max, and average temperatures.  The pictures are then displayed on
a map using the GPS data from the jpg fils.


### Images needed
1) JPEG images where temperature is represented by RGB colors from the Viridis color palette. The darkest blue is 0 degrees Celsius or less and the brightest yellow is 80 degrees Celsius or greater. JPEGS contain GPS coordinates in the EXIF meta data.

2) TIFF images where every pixel is the temperature in Celsius.
