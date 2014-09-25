PIC TO ASCII
############

This script requires the Pillow library
It can be installed with Pip or Easy_Install or can be downloaded at:
https://pypi.python.org/pypi/Pillow/2.5.3

This script is designed to be run from a command line interface. 

usage: ASCII.py [-h] [-j] [-i] [-w WIDTH] filename

positional arguments:
  filename    path of image to be viewed

optional arguments:
  -h, --help  show this help message and exit
  -j          Turn off hdr - By default the contrast will be altered so that
              the image uses the entire colorspace. This option prevents that
  -i          invert the image - this is used if displaying dark text on a
              white background
  -w WIDTH    width of the image in pixels (must be an integer)

The set of characters used for shading can be found in letterset.ini. The
default letterset is "@%#x+=:- ". However a custom set can be used by modifying
the file to any string of ASCII characters ordered from darkest to lightest.