#For Python3
from PIL import Image, ImageStat
import sys
import os
import re

#Dimension Enum
class dim:
    x = 0
    y = 1

#Get FileName function
def listFiles (ls):
    imageList = []
    for i in range (0, len (ls) ):
        if ( re.search ("\.(jpe?g|gif|png|bmp|tiff)$", ls[i]) ):
            print ( str(len(imageList)) + ". " + ls[i])
            imageList.append (ls[i])
    if ( len(imageList) == 0):
        _ = input("Error: No image files found")
        exit()
    if ( len(imageList) == 1):
        return imageList[0]
    while (True):
        index = getInteger("Enter selection number: ")
        if (index < len(imageList) and index >= 0):
            return imageList[ index ]
        print ("Error: input must be between %s and %s\n" % (0, len(imageList)-1) )

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
def fitToConsole (image):
    consoleSize = (os.get_terminal_size()[dim.x], round (os.get_terminal_size()[dim.y] /2) *4)
    consoleRatio = consoleSize[dim.x] / consoleSize[dim.y]
    imageRatio = image.size[dim.x] / image.size[dim.y]
    limit = None
    if (consoleRatio / imageRatio <= 1):
        limit = 'horizantal'
        width = consoleSize[dim.x]
        height = round( width / imageRatio /2 ) *2
    else:
        limit = 'vertical'
        height = consoleSize[dim.y]
        width = round(height * imageRatio /2) *2
    return (image.resize((width, height)), limit)

#Load Letterset Function
def getLetterset():
    defaultLetterset = "@%#x+=:- "
    try:
        lettersetFile = open("letterset.ini", 'r+')
        letterset = lettersetFile.read()
        if ( len(letterset) < 2):
            print ("Error: letterset too short. Reverting to default")
            lettersetFile.write(defaultLetterset)
            letterset = defaultLetterset
    except:
        print ("Error: letterset.ini not found: creating new file")
        lettersetFile.write(defaultLetterset)
        letterset = defaultLetterset
    finally:
        lettersetFile.close()
    return letterset

#Prompt User / Set variables
print ("Image files in current directory:")
imageName = listFiles ( os.listdir() )
name = re.match( "(.+)\.", imageName )
hdr = input ("Apply HDR? (y/n): ")
invert = input ("Invert image? (y/n): ")
text = ""

letterset = getLetterset()

#Load image and convert to greyscale
image = Image.open (imageName)
image = image.convert ('L')

(image, limit) = fitToConsole(image)

#Apply Effects
data = []
stats = ImageStat.Stat(image)
[(min, max)] = stats.extrema
for y in range (0, image.size[dim.y]):
    for x in range (0, image.size[dim.x]):
        pixel = image.getpixel ((x,y))
        if (hdr != 'n'):
            offset = min - 0
            stretch = 255 / max
            pixel = (pixel - offset) * stretch
        if invert == 'y': pixel = 255 - pixel
        data.append (pixel)
image = Image.new ('L', image.size)
image.putdata (data)

#Generate ASCII
for y in range ( 0, image.size[dim.y], 2 ):
    for x in range ( 0, image.size[dim.x] ):
        brightness = ( image.getpixel(( x, y)) + image.getpixel((x,y+1)) ) / 2
        index = round( (brightness / 255) * len(letterset) ) -1
        text += letterset[ index ]
    if limit =='vertical': text += '\n' 

#Write to File
print (text)
