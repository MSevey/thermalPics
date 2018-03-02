Raptor Maps Mini Coding Challenge.

These images may not be distributed, published, or discussed with any party other than current Raptor Maps employees unless explicit written permission is provided by the Raptor Maps CEO.

Images:

Two directories are provided of the same data.

1) JPEG images where temperature is represented by RGB colors from the Viridis color palette. The darkest blue is 0 degrees Celsius or less and the brightest yellow is 80 degrees Celsius or greater. JPEGS contain GPS coordinates in the EXIF meta data.
Viridis: https://matplotlib.org/examples/color/colormaps_reference.html

2) TIFF images where every pixel is the temperature in Celsius.

Raptor Maps Inc (c) 2017


Steps:
1) read images, both jgp and tiff format.  get temps from tiff and GPS info from jpg.
  store information in database

2) display images as pins on a map 
