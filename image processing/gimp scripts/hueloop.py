#!/usr/bin/env jython

import os, sys
from javax.imageio import ImageIO
from java.awt.image import BufferedImage
from java.awt import Color
from java.io import File
from java.lang.Math import *

print sys.argv
ifile = sys.argv[1]
print ifile

N = 12

fname = ifile.split('/')[-1].split('.')[0]
print fname

try:
	os.mkdir('%s_hueloop'%fname)
except Exception, e:
	print e

img1 = ImageIO.read(File(ifile));

def rotateImage(img,th):
	img3 = BufferedImage(img1.width,img1.height,BufferedImage.TYPE_INT_RGB)
	Q1 = sin(th)/sqrt(3)
	Q2 = (1-cos(th))/3
	for i in xrange(img1.height):
		for j in xrange(img1.width):
			rgb1 = Color(img.getRGB(j,i))
			r = rgb1.red  
			g = rgb1.green
			b = rgb1.blue 
			rb = r-b
			gr = g-r
			bg = b-g
			r1 = Q2*(gr-rb)-Q1*bg+r
			Z  = Q2*(bg-rb)+Q1*gr
			g += Z + (r-r1)
			b -= Z
			r = r1
			r = 0 if r<0 else 255 if r>255 else int(r)
			g = 0 if g<0 else 255 if g>255 else int(g)
			b = 0 if b<0 else 255 if b>255 else int(b)
			img3.setRGB(j,i,Color(r,g,b).RGB)
	return img3

for H in range(N):
	print H
	img3 = rotateImage(img1, 2*PI*H/N)
	ImageIO.write(img3,"png",File("%s_hueloop/out_%d.png"%(fname,H)))
