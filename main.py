import scipy as sp
import numpy as np
from scipy import misc
from scipy import ndimage
import argparse
import matplotlib.pyplot as plt
import random
import unicodedata
import os
import sys

if sys.platform == 'posix':
	import Image,ImageDraw,ImageFont
else:
	# This should also work on *nix machines. Check.
	from PIL import Image,ImageDraw,ImageFont

import time
from sklearn.neighbors import KNeighborsClassifier

def edges(image):
	""" Returns the edges of an image, using the sobel operator in two dimensions"""
	sx = ndimage.filters.sobel(image, axis=0)
	sy = ndimage.filters.sobel(image, axis=1)
	return np.hypot(sx, sy)

def padSides(image, x, y):
	""" Pads out the edges of an image to divide cleanly"""
	if y%res != 0:
		dy = res-(y%res)
	else:
		dy = 0
	if x%res != 0:
		dx = res-(x%res)
	else:
		dx = 0
	print(dy, dx)
	image = np.pad(sob,((0,dy),(0,dx)),'constant', constant_values=(0))
	print("new shape", image.shape)
	xs = (x/res)+1
	ys = (y/res)+1

	return np.chararray((ys, xs), unicode=True)

def generateCharBitmap(char, pad=0):
	""" Given an input string, return an array representing the corresponding bitmap"""
	# Note that point - pixel conversion means these will all be slightly small for now
	#print(char)
	# Special case
	if char == '':
		return [0] * res**2
	x1, y1 = font.getsize(char)
	a, b = font.getoffset(char)
	if pad == 0:
		return np.reshape(np.asarray(font.getmask(char, mode="1")), (y1-b,x1-a))
	else:
		aa = np.reshape(np.asarray(font.getmask(char, mode="1")), (y1-b,x1-a))
		# This is hacky and bad, but for now avoids abberant letters that are too big
		newX = 0 if x1 - a < 0 or x1 - a > res else x1 - a
		newY = 0 if y1 - b < 0 or y1 - b > res else y1 - b
		aa = np.pad( aa , (	(( res-newY )/2, ( res-newX )/2), ((res-newY+1)/2 , (res-newX+1)/2)), 'minimum')
		# plt.imshow(aa)
		# plt.show()
		aa = np.resize(aa, (res**2))
		return aa




t0 = time.time()
parser = argparse.ArgumentParser()
parser.add_argument("fileName", help="File to load", type=str)
parser.add_argument("res", help="Size of pixel square to use", type=int)
parser.add_argument("hashBins", help="Number of hashing bins. Lower = slower, higher = looks worse but more accurate?", type=int)
args = parser.parse_args()

image = sp.misc.imread(args.fileName,flatten=True) #WHY DOES THIS WORK!!??
res = args.res
hashs = args.hashBins
#image = misc.lena()

sob = edges(image)
y, x =  image.shape
out = padSides(image, x, y)
ys, xs = out.shape





render 	= ['#','|','-','','/','\\', '(', #u"\u2610",
 ')','{','}','[',']','1','2','3','4','5','6','7',
 '8','9','0','q','w','e','r','t','y','u','i','o',
 'p','a','s','d','f','g','h','j','k','l',';',"'",'z','x','c','v','b','n','m',',',
 '.','/','`','"','!','@','#','$','%','^','&','*','+','=','_']
# render = ['#','|','/','\\','-', ' ']
comp 	= []

font = ImageFont.truetype("OpenSans-Regular.ttf", int(res*92/76))

for index in range(len(render)):
	x = generateCharBitmap(render[index], 1)
	#engine.store_vector(x, render[index])
	comp.append(x)

t1 = time.time()

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(comp, render)
#array = generateCharBitmap('R', 1)

#print(knn.predict([array]))




y, x =  image.shape
for j in xrange(0,y,res):
	for i in xrange(0,x,res):
		array = sob[j:j+res, i:i+res]
		if len(np.hstack(array)) < res**2:
			array = np.append(array,([0]*(res**2-len(np.hstack(array)))))
		oute = knn.predict([np.hstack(array)]) #compare2(array)
		#print('sel: ', oute)
		out[(j/res),(i/res)] = oute[0]
canvas2 = Image.new('RGB', (x+100, y+100), (255, 255, 255))
draw = ImageDraw.Draw(canvas2)
for j in range(0,ys):
	for i in range(0,xs):
		#print(i,j)
		a = unicode(out[j, i])
		# This is using <x,y> in contrast to everything else
		draw.text((i*res+10,j*res+5), a, font = font, fill = "#000000")
t1 = time.time()

total = t1-t0
print("time taken ",total)
plt.imshow(canvas2)
plt.show()
#plt.imshow(sob)
#plt.show()