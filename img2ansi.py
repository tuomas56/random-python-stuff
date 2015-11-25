"""
Usage: img2txt.py <imgfile> [--maxLen=<maxLen>] [--fontSize=<fontSize>] [--color]

"""

import sys

from ansi.color.rgb import rgb256
from ansi.color.fx import reset

from docopt import docopt
from PIL import Image

dct = docopt(__doc__)

imgname = dct['<imgfile>']

maxLen = dct['--maxLen']

clr = dct['--color']

fontSize = dct['--fontSize']

try:
    maxLen = float(maxLen)
except:
    maxLen = 100.0   # default maxlen: 100px

try:
    fontSize = int(fontSize)
except:
    fontSize = 7



try:
    img = Image.open(imgname)
except IOError:
    exit("File not found: " + imgname)

# resize to: the max of the img is maxLen

width, height = img.size

rate = maxLen / max(width, height)

width = int(rate * width)  # cast to int

height = int(rate * height)

img = img.resize((width, height))

img = img.convert('L')

# get pixels
pixel = img.load()

# grayscale
color = "MNHQ$OC?7>!:-;. "

string = ""

for h in range(height):  # first go through the height,  otherwise will roate
    for w in range(width):
        rgb = pixel[w, h]
        if clr:
            string += str(rgb256(*rgb)) + '▇' + str(reset)
        else:
            string += color[int(sum(rgb) / 3.0 / 256.0 * 16)]
    string += "\n"

print(string)