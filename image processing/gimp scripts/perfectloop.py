#!/usr/bin/env jython

import os, sys
from javax.imageio import ImageIO
from java.awt.image import BufferedImage
from java.awt import Color
from java.io import File

print sys.argv
directory = sys.argv[1]
files = sorted([f for f in os.listdir(directory) if '.png' in f])
print files
assert len(files)&1==0
midpoint = len(files)/2

set1,set2 = files[:midpoint],files[midpoint:]

weights = [int(256.*x/(midpoint+1)) for x in range(midpoint)]

os.mkdir(directory+'_looped')

for ii,(f1,f2,alpha) in enumerate(zip(set1,set2,weights)):
	print ii
	img1 = ImageIO.read(File(directory+'/'+f1));
	img2 = ImageIO.read(File(directory+'/'+f2));
	assert img1.width==img2.width and img1.height==img2.height
	img3 = BufferedImage(img1.width,img1.height,BufferedImage.TYPE_INT_RGB)
	beta = 256-alpha
	for i in xrange(img1.height):
		for j in xrange(img1.width):
			rgb1 = Color(img1.getRGB(j,i))
			rgb2 = Color(img2.getRGB(j,i))
			r = rgb1.red  *alpha + rgb2.red  *beta + 0x80 >> 8
			g = rgb1.green*alpha + rgb2.green*beta + 0x80 >> 8
			b = rgb1.blue *alpha + rgb2.blue *beta + 0x80 >> 8
			img3.setRGB(j,i,Color(r,g,b).RGB)
	ImageIO.write(img3,"png",File(directory+"_looped/out_%d.png"%ii))


'''
Do the rest with gimp scripting:
-- open as layers all output images
-- convert to index with [selected color pallet]
-- save as animated gif

gimp -b

There is no procedure for "open as layers". Instead we will have to open
each image individually, and add them as layers one by one.

First, open the first image as you normally would

(let (image (gimp-file-load RUN-NONINTERACTIVE "ABSOLUTEPATHTOIMATE" "ABSOLUTEPATHTOIMATE"))
	
)

gimp_file_load_layer ()

Loads an image file as a layer for an existing image.

This procedure behaves like the file-load procedure but opens the specified
image as a layer for an existing image. The returned layer needs to be
added to the existing image with gimp_image_add_layer().

run_mode :	The run mode. RUN-NONINTERACTIVE 1
image_ID :	Destination image.
filename :	The name of the file to load.
Returns  :	The layer created when loading the image file. 

'''




