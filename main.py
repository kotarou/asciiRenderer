import scipy as sp
import numpy as np
from scipy import misc
from scipy import ndimage
import argparse
import matplotlib.pyplot as plt
import Image,ImageDraw,ImageFont
import random
import unicodedata
import os


parser = argparse.ArgumentParser()
parser.add_argument("fileName", help="display a square of a given number", type=str)
parser.add_argument("res", help="display a square of a given number", type=int)
args = parser.parse_args()

image = sp.misc.imread(args.fileName,flatten=True) #WHY DOES THIS WORK!!??
res = args.res
#image = misc.lena()

sx = ndimage.filters.sobel(image, axis=0)
sy = ndimage.filters.sobel(image, axis=1)

sob = np.hypot(sx, sy)
avg = np.average(sob)

vals = sob.shape
y = vals[0]
x = vals[1]
print("old shape", sob.shape)



if y%res != 0:
	dy = res-(y%res)
else:
	dy = 0
if x%res != 0:
	dx = res-(x%res)
else:
	dx = 0
print(dy, dx)
sob = np.pad(sob,((0,dy),(0,dx)),'constant', constant_values=(0))
print("new shape", sob.shape)
#sob[sob == ''] = 0
# Remember that these are going to be opposite
# ie, .shape gives (y,x)
print("width",x, " height", y)

# plt.imshow(sob, cmap='Greys_r')
# plt.show()

xs = (x/res)+1
ys = (y/res)+1

out = np.chararray((ys, xs), unicode=True)
print("shape of output ", out.shape)


render 	= ['#','|','-','','/','\\', u"\u2610",'(',
')','{','}','[',']','1','2','3','4','5','6','7',
'8','9','0','q','w','e','r','t','y','u','i','o',
'p','a','s','d','f','g','h','j','k','l',';',"'",'z','x','c','v','b','n','m',',',
'.','/','`','"','!','@','#','$','%','^','&','*','+','=','_',]
comp 	= []


font = ImageFont.truetype("OpenSans-Regular.ttf", int(res*1.2))

# How about I make this a one off for each time I choose a new resolution?
if os.path.isdir('textRenders_'+str(res)):
	print("Images exist")
	# load images into comp
else:
	print("Images do not exist")
	# implment behaviour here

for target in render:
	canvas = Image.new('L', (res, res), "black")
	draw = ImageDraw.Draw(canvas)
	# This is using <x,y> in contrast to everything else
	draw.text((1,-res/2), target, font = font, fill = "white")
	comp.append(canvas)
	# plt.imshow(canvas, cmap='Greys_r')
	# plt.show()

def compare(arr):
	"""Takes an input array and returns the ascii character that best represents it"""
	mseMax = 999999999
	use = ''
	for i in range(0,len(render)):
		#print(type(comp[i]))
		err = np.sum((comp[i] - arr) ** 2)
		if err < mseMax:
			mseMax = err
			use = render[i]
	return use

	#return render[random.randint(0,1)]

	# if np.average(array) > avg:
	# 	return "0"
	# else:
	# 	return "1"


for j in xrange(0,y,res):
	for i in xrange(0,x,res):
		array = sob[j:j+res, i:i+res]
		out[(j/res),(i/res)] = compare(array)

canvas2 = Image.new('RGB', (x+100, y+100), (255, 255, 255))
draw = ImageDraw.Draw(canvas2)
for j in range(0,ys):
	for i in range(0,xs):
		#print(i,j)
		a = unicode(out[j, i])
		# This is using <x,y> in contrast to everything else
		draw.text((i*res+10,j*res+5), a, font = font, fill = "#000000")

plt.imshow(canvas2)
plt.show()
#plt.imshow(sob)
#plt.show()