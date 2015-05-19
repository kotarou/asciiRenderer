import scipy as sp
import numpy as np
from scipy import misc
from scipy import ndimage
import argparse
import matplotlib.pyplot as plt
import Image,ImageDraw,ImageFont


def compare(arr):
	"""Takes an input array and returns the ascii character that best rperesents it"""
	if np.average(array) > avg:
		return "0"
	else:
		return "1"

parser = argparse.ArgumentParser()
#parser.add_argument("fileName", help="display a square of a given number", type=str)
parser.add_argument("res", help="display a square of a given number", type=int)
args = parser.parse_args()

#image = sp.misc.imread(args.fileName)
res = args.res
image = misc.lena()

sx = ndimage.filters.sobel(image, axis=0)
sy = ndimage.filters.sobel(image, axis=1)

sob = np.hypot(sx, sy)
avg = np.average(sob)

vals = sob.shape
print(vals)
# Remember that these are going to be opposite
# ie, .shape gives (y,x)
y = vals[0]
x = vals[1]
print("width",x, " height", y)



xs = (x/res)+1
ys = (y/res)+1

out = np.zeros((ys, xs))
print("shape of output ", out.shape)
render ={'0','1'}



for j in xrange(0,y,res):
	for i in xrange(0,x,res):
		array = sob[j:j+res, i:i+res]
		out[(j/res),(i/res)] = compare(array)


font = ImageFont.truetype("OpenSans-Regular.ttf", res)

canvas = Image.new('RGB', (x+100, y+100), (255, 255, 255))
draw = ImageDraw.Draw(canvas)
for j in range(0,ys):
	for i in range(0,xs):
		#print(i,j)
		a = str(int(out[j, i]))
		# This is using <x,y> in contrast to everything else
		draw.text((i*res+10,j*res+5), a, font = font, fill = "#000000")

plt.imshow(canvas)
plt.show()
#plt.imshow(sob)
#plt.show()