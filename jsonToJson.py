import json
import os
import sys
import plistlib
import re
import shutil
def numberOfCode(arr,path):
        for dir in os.listdir(path):
		if os.path.isfile(path+dir):
			if dir[-5:] == ".json"or dir[-6:] =='.plist' or dir[-11:] == '.ExportJson':
				arr.append(dir)
			
        return arr

def getResUrl(root):
		name = os.path.basename(os.path.realpath(root));
		urlName = name 
		while "res"!= name and name!= 'animation':
			root = os.path.abspath(os.path.dirname(root)+os.path.sep+".");
			name = os.path.basename(os.path.realpath(root));
			if name !='res':
				urlName=name+'.'+urlName;
		return urlName
def getMoveTextUrl(url):
		moveUrl = ''
		os.chdir(os.path.pardir)
		name = os.path.basename(os.path.realpath(url));
		for file in os.listdir(os.getcwd()): 
			if name.split('client')[0]+'art'==file:
				moveUrl = os.getcwd()+'/'+file+'/animation'
		os.chdir(url)
		return moveUrl
def writeTxt(jsongrouper,jsonUrl):
		for root, dirs, files in os.walk(jsonUrl, topdown=False):
			url = root + '/'
			arr = []
			numberOfCode(arr,url)
			if len(arr)>0:
				name = getResUrl(root)
				for i in arr:
					name1 = '@'+ name + '.'+i+'#'
					fb = open(url+i,'r')
					jsongrouper.write(name1)
					if i[-11:] == '.ExportJson' or i[-5:] == ".json":
						dicts = json.load(fb)
						json.dump(dicts,jsongrouper)
					if i[-6:] =='.plist' :
						for  line in  fb.readlines(): 
							jsongrouper.write(line.strip("\n").strip("\r").strip("\t").strip(" "))
					fb.close()
					#if jsonUrl[-4:]=="/res":
						#os.remove(url+i)
			#if not os.listdir(root):
				#os.removedirs(root)
			arr = []

os.chdir(os.path.pardir)

txtUrl = os.getcwd() + '/res/ui/'
jsonGrouper = txtUrl +"data.txt"
if os.path.isfile(jsonGrouper):
	os.remove(jsonGrouper) 
if not os.path.exists(txtUrl):
	os.makedirs(txtUrl)
jsongrouper = open(jsonGrouper,'w')
writeTxt(jsongrouper,getMoveTextUrl(os.getcwd()))
writeTxt(jsongrouper,os.getcwd()+"/res")
jsongrouper.close()
os.chdir(os.getcwd()+"/tools")
os.system("python findFiles.py")