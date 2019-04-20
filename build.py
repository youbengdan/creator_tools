# -*- coding: UTF-8 -*-
import os
import sys
import time
import shutil
def search(path,name):
	#print(name)
	for root, dirs, files in os.walk(path):  # path 为根目录
		if name in dirs or name in files:
			flag = 1      #判断是否找到文件
			root = str(root)
			
			return os.path.join(root, name)
	return -1

name = 'moka_'
num = '1'

if len(sys.argv) == 2 :
	num = sys.argv[1]
name+=num
name1 = 'InnerServer'
if num == '1' :
	name1 = 'OutServer'
if num =='1':
	name+='_release_'
else:
	name+='_test_'

path = os.getcwd();

print (name)
print (time.strftime("%H:%M:%S"))
result = os.popen("ant js -Dch="+num)
print (result.read())
print (time.strftime("%H:%M:%S"))

path = os.getcwd();
folder = path + '/update/ch'+num
if not os.path.exists(folder):
	os.makedirs(folder)
	 
os.chdir("frameworks/runtime-src/proj.android")
os.system("gradle assemble"+name1) 

print (time.strftime("%H:%M:%S"))

answer = search(os.getcwd(),'moka-client-'+name1+'-release.apk')
if answer == -1:
    print("没找到APK文件")
else:
	folder = path + '/app'
	if not os.path.exists(folder):
		os.makedirs(folder)
	shutil.move(answer,folder +'/'+name+time.strftime("%Y%m%d")+'.apk')





