#!/usr/bin/python -B
# -*- coding:utf-8 -*-

import sys
import shutil
import os
import zipfile
import cStringIO
import multiprocessing
import re
import string
import random
import platform
import math
import os
import os.path

# import DirToZip;
# import distutils.dir_util
# import ImageAlpha_Packet;
import time

#main call
if __name__ == "__main__" :


     #当前路径
    script_dir = sys.path[0]
    project_dir =os.path.abspath(os.path.dirname(script_dir)+os.path.sep+"..")

    try:
        resDir = sys.argv[1]
    except:
        print "python pack_resource.py need "
        print "use th default 'res' "
        resDir = "./res/"##proj.google_portrait.android
    resDir = project_dir + resDir


    try:
        f = sys.argv[2]
    except:
        print "python pack_resource.py need "
        print "use th default 'jsList.js' "
        f = "./src/jsList.js"##proj.google_portrait.android
    f = project_dir + f
    f_name = os.path.basename(f)
    f_name = f_name[0:f_name.index('.')]


	#获取操作系统名称及版本号，’Windows-7-6.1.7601-SP1′ 
    platformStr = platform.platform()
    nPos = platformStr.find("Windows")
    print platformStr
    if nPos < 0 :
    	print "this is not windows "
    else :
    	print "this is windows"
    print "begin pack_android"

    print(resDir);


    str = ""
    str +="\n var " +f_name+ " = ["
    for parent,dirnames,filenames in os.walk(resDir):
        for filename in filenames:
            if not (".DS_Store") in filename and not (".mp3") in filename and not (".ttf") in filename:
                file = os.path.join(parent,filename)
                if not ("\\src\\") in file and not ("/src/") in file:
                    file = file[((file.find('/',1))+1):]
                    str += "\n\t\""+file+"\","

    str+="\n];"
    print str

    
    output = open(f, 'wb')
    str=str.replace("\\","/")
    output.write(str)
    output.close()

    print 'all done!'


