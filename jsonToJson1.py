# -*- coding: utf-8 -*-  
import json
import os
import sys
import plistlib
import re
import shutil
import codecs
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
def getUrlName(root,stop,stopbol,char):
		name = os.path.basename(os.path.realpath(root));
		urlName = name 
		while stop!= name :
			root = os.path.abspath(os.path.dirname(root)+os.path.sep+"/");
			name = os.path.basename(os.path.realpath(root));
			if stopbol == 1 or name != stop:
				urlName=name+char+urlName;
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
def replacePNG_Name(line,root,fileName):
		string = '';
		name = '';
		n=0;
		nn = 0;
		nameArr = [];
		while n<len(line):
			name = ''
			if line[n]=='.'and line[n+1]=='p'and line[n+2]=='n'and line[n+3]=='g' and line[n+4]=='<':
				m = n;
				while m>0:
					m = m-1;
					if line[m] =='>':
						break;
					name = line[m] + name;
				fileName1 = fileName.split('.')[0]
				if name != fileName1 : 
					name1 = name.split('/')
					l = len(name1)
					if l>=3:
						break
					nameArr.append(name)

					while m>=nn:
						string = string+line[nn];
						nn = nn+1;
						#print line[nn],line[m]
					nn = n;
					string = string + getUrlName(root,'res',0,'_')+'___'+name;
					print root,name,name1[l-2],fileName1
			n=n+1;
					#print root,name,nameArr
			
		# for i in nameArr:
		# 	string.replace('>'+i+'.png<','>'+root+'/'+i+'.png<')
		# 	print '>'+i+'.png<','>'+root+'/'+i+'.png<',root,fileName
		while nn<len(line):
			string = string+line[nn];
			nn=nn+1
		return string;
def writeTxt(jsongrouper,jsonUrl):
		for root, dirs, files in os.walk(jsonUrl, topdown=False):
			url = root + '/'
			arr = []
			numberOfCode(arr,url)
			if len(arr)>0:
				name = getResUrl(root)
				for i in arr:
					name1 = '@'+ name + '.'+i+'#'
					if not os.path.isfile(url+i):
						break;
					fb = open(url+i,'r+')
					jsongrouper.write(name1)
					if i[-11:] == '.ExportJson' or i[-5:] == ".json":
						dicts = json.load(fb)
						json.dump(dicts,jsongrouper)
					if i[-6:] =='.plist' :
						string = '';
						for  line in  fb.readlines(): 
							line = replacePNG_Name(line,getUrlName(root,'res',1,'/'),i)
							string = string+line
							jsongrouper.write(line.strip("\n").strip(' '))

						fb.close()
						os.remove(url+i)
						f = open(url+i,'w')
						f.write(string)
						f.close()
						
					fb.close()
					#if jsonUrl[-4:]=="/res":
					#	os.remove(url+i)
			# if not os.listdir(root):
			# 	os.removedirs(root)
			arr = []

os.chdir(os.path.pardir)

txtUrl = os.getcwd() + '/res/ui/'
jsonGrouper = txtUrl +"data.txt"
if os.path.isfile(jsonGrouper):
	os.remove(jsonGrouper) 
if not os.path.exists(txtUrl):
	os.makedirs(txtUrl)
jsongrouper = open(jsonGrouper,'w')
writeTxt(jsongrouper,os.getcwd()+"/res")
jsongrouper.close()
# os.chdir(os.getcwd()+"/tools")
# os.system("python findFiles.py")