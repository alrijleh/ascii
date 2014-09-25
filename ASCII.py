#For Python3
import sys
import argparse
import os
import re

from PIL import Image, ImageStat

class dim:
    """Dimension Enumerator"""
    x = 0
    y = 1

def round (number):
    """Rounds a float to an int"""
    diff = number - int(number)
    if (diff < .5):
        return int(number)
    else:
        return int(number) +1

def resize (image, width):
    """Resize image to specified size or console"""
    add_newline = True
    if width:
        scale_factor = width / image.size[dim.x]
        height = round(scale_factor * image.size[dim.y] /2) *2
        image = image.resize((width,height))
    else:
        console_size = (os.get_terminal_size()[dim.x], round (os.get_terminal_size()[dim.y] /2) *4)
        console_ratio = console_size[dim.x] / console_size[dim.y]
        image_ratio = image.size[dim.x] / image.size[dim.y]
        limit = None
        if (console_ratio / image_ratio <= 1):
            width = console_size[dim.x]
            height = round(width / image_ratio /2) *2
            add_newline = False
        else:
            height = console_size[dim.y]
            width = round(height * image_ratio /2) *2
    return (image.resize((width, height)), add_newline)

def get_letterset():
    """Load the letterset from file"""
    default_letterset = " -:=+x#%@"
    path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(path, 'letterset.ini')
    try:
        letterset_file = open(filepath, 'r+')
        letterset = letterset_file.read()
        if ( len(letterset) < 2):
            print ("Error: letterset too short. Reverting to default")
            letterset_file.write(default_letterset)
            letterset = default_letterset
    except:
        print ("Error: letterset.ini not found: creating new file")
        letterset_file = open(filepath, 'w')
        letterset_file.write(default_letterset)
        letterset = default_letterset
    finally:
        letterset_file.close()
    return letterset

def modify_image(image, hdr, invert):
    """Apply affects to the image"""
    data = []
    stats = ImageStat.Stat(image)
    [(min, max)] = stats.extrema
    for y in range (0, image.size[dim.y]):
        for x in range (0, image.size[dim.x]):
            pixel = image.getpixel ((x,y))
            if hdr:
                offset = min - 0
                stretch = 255 / max
                pixel = (pixel - offset) * stretch
            if invert:
                pixel = 255 - pixel
            data.append (pixel)
    new_image = Image.new ('L', image.size)
    new_image.putdata (data)
    return new_image

def ascii(image, letterset, add_newline):
    """Generate ascii text from the image"""
    text = ""
    for y in range ( 0, image.size[dim.y], 2 ):
        for x in range ( 0, image.size[dim.x] ):
            brightness = ( image.getpixel(( x, y)) + image.getpixel((x,y+1)) ) / 2
            index = round( (brightness / 255) * len(letterset) ) -1
            text += letterset[ index ]
        if add_newline:
            text += '\n'
    return text


def open_image(filename):
    """Opens an image file and returns an image object"""
    try:
        image = Image.open(filename).convert('L')
    except:
        sys.exit("Error: could not open " + filename)
    return image


def get_args():
    """Gets arguments from command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', help="Turn off hdr - By default the contrast will be altered so that the image uses the entire colorspace. This option prevents that", action='store_false', default=True, dest='hdr')
    parser.add_argument('-i', help="invert the image - this is used if displaying dark text on a white background", action='store_true', default=False, dest='invert')
    parser.add_argument('-w', help="width of the image in pixels (must be an integer)", type=int, default=0, dest='width')
    parser.add_argument('filename', help='path of image to be viewed')
    args = parser.parse_args()
    return args

#Main
def main():
    args = get_args()
    letterset = get_letterset()
    image = open_image(args.filename)
    image, add_newline = resize(image, args.width)
    image = modify_image(image, args.hdr, args.invert)
    text = ascii(image, letterset, add_newline)
    print (text)

if __name__ == "__main__":
    main()
