import os,sys
import os.path
import platform

#需要过滤的文件
notActionFile = ["00000.png"]
#需要过滤的文件夹
notActionPath = ["0000"]

#需要删除的文件
needDeleteFile = ["00000.png"]


def file_extension(path): 
  return os.path.splitext(path)[1] 

  
print(platform.system())
rootdir = sys.argv[1]
if len(sys.argv)==3:
  rootdir = sys.argv[2]

print rootdir
a = '/';
pngquantPath = '/pngquant/mac/'
if(platform.system()=='Windows'):
    a = '\\';
    pngquantPath = '/pngquant/win/'

for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        fullPath = os.path.join(parent,filename)
        #删除文件
        for deleteFile in needDeleteFile:
           if  filename == deleteFile: 		
              os.remove(fullPath)			  
        isFilter = False
        #过滤文件压缩
        for noActionName in notActionFile:	
          if noActionName == filename:
              isFilter = True
        #过滤文件夹压缩			  
        for onePath in notActionPath:
          lastPath = fullPath.split(a)[-2]
          if lastPath == onePath:
              isFilter = True              		   
        if file_extension(fullPath) == ".png" and isFilter == False:
          print "action"		
          os.system(os.getcwd()+pngquantPath+"pngquant -f --ext .png --quality 85-95 \"" + fullPath  + "\"")
          print fullPath
	