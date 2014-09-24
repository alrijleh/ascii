#For Python3
import sys
import argparse
import os
import re

from PIL import Image, ImageStat

#Dimension Enum
class dim:
    x = 0
    y = 1

#Get FileName function
def list_files (ls):
    image_list = []
    for i in range (0, len (ls) ):
        if ( re.search ("\.(jpe?g|gif|png|bmp|tiff)$", ls[i]) ):
            print ( str(len(image_list)) + ". " + ls[i])
            image_list.append (ls[i])
    if ( len(image_list) == 0):
        _ = input("Error: No image files found")
        exit()
    if ( len(image_list) == 1):
        return image_list[0]
    while (True):
        index = getInteger("Enter selection number: ")
        if (index < len(image_list) and index >= 0):
            return image_list[index]
        print ("Error: input must be between %s and %s\n" % (0, len(image_list)-1) )

#Get integer from user input
def getInteger(query):
    while (True):
        try:
            return int( input(query) )
        except:
            print ("Error: input must be an integer\n")

#Rounding function
def round (number):
    diff = number - int(number)
    if (diff < .5):
        return int(number)
    else:
        return int(number) +1

#Fit to console
def fit_to_console (image):
    console_size = (os.get_terminal_size()[dim.x], round (os.get_terminal_size()[dim.y] /2) *4)
    console_ratio = console_size[dim.x] / console_size[dim.y]
    image_ratio = image.size[dim.x] / image.size[dim.y]
    limit = None
    if (console_ratio / image_ratio <= 1):
        limit = 'horizantal'
        width = console_size[dim.x]
        height = round(width / image_ratio /2) *2
    else:
        limit = 'vertical'
        height = console_size[dim.y]
        width = round(height * image_ratio /2) *2
    return (image.resize((width, height)), limit)

#Load Letterset Function
def get_letterset():
    default_letterset = "@%#x+=:- "
    try:
        letterset_file = open("letterset.ini", 'r+')
        letterset = letterset_file.read()
        if ( len(letterset) < 2):
            print ("Error: letterset too short. Reverting to default")
            letterset_file.write(default_letterset)
            letterset = default_letterset
    except:
        print ("Error: letterset.ini not found: creating new file")
        letterset_file.write(default_letterset)
        letterset = default_letterset
    finally:
        letterset_file.close()
    return letterset

#Apply Effects
def modify_image(image, hdr, invert):
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

#Generate ASCII
def ascii(image, limit):
    text = ""
    for y in range ( 0, image.size[dim.y], 2 ):
        for x in range ( 0, image.size[dim.x] ):
            brightness = ( image.getpixel(( x, y)) + image.getpixel((x,y+1)) ) / 2
            index = round( (brightness / 255) * len(letterset) ) -1
            text += letterset[ index ]
        if (limit =='vertical'):
            text += '\n'
    return text

#Main
parser = argparse.ArgumentParser()
parser.add_argument('-j', action='store_false', default=True, dest='hdr')
parser.add_argument('-i', action='store_true', default=False, dest='invert')
parser.add_argument('filename')

options = parser.parse_args()
print (options)

letterset = get_letterset()
image = Image.open (options.filename).convert('L')
(image, limit) = fit_to_console(image)
image = modify_image(image, options.hdr, options.invert)
text = ascii(image, limit)
print (text)