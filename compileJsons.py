#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path

#rootDir="./"
rootDir="../"

resDir = rootDir + "res"

def dealFile(filename):
	print rootDir + filename
	fo = open(rootDir + filename,"r")
	str = ""
	while True:
		line = fo.readline()
		if len(line)==0:
			break
		str = str + line
	if (".json") in filename or (".ExportJson") in filename:
		str = str.replace(" ","")
	str = str.replace("\t","")
	str = str.replace("\r","")
	str = str.replace("\n","")
	fo.close()
	fo = open(rootDir + filename,"wb")
	fo.write(str)
	fo.close()

str="//this file is create auto by 'findFiles.py'"
str+="\nvar g_resources = ["

for parent,dirnames,filenames in os.walk(resDir):
    for filename in filenames:
        if not (".DS_Store") in filename and not (".mp3") in filename and not (".png") in filename and not (".manifest") in filename and not (".fnt") in filename and not (".ttf") in filename:
        	file = os.path.join(parent,filename)
        	file = file[((file.find('/',1))+1):]
        	dealFile(file)
        	str += "\n\t\""+file+"\","

str+="\n];"
#print str

output = open(rootDir + 'tools/alljsons.js', 'wb')
output.write(str)
output.close()

print 'all done!'