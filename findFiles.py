import os
import os.path
import hashlib
import datetime
import sys
import time

rootDir="../"

params1 = {"updateCache":False,"noLog":False,"md5" : False}
params2 = {"destDir" : "res", "exportDir" : "src", "h5Dir" : "build_res/h5/", "ignoreRoot" : ""}

defaultCacheFiles={};
# defaultCacheFiles[h5Dir + 'css/style.css'] = "css/style.css";
# defaultCacheFiles['build/build_4_jsb/game.js'] = "js/game.js";
# defaultCacheFiles[h5Dir + 'js/HBuilder.js'] = "js/HBuilder.js";
# defaultCacheFiles[h5Dir + 'js/resource.js'] = "js/resource.js";
# defaultCacheFiles[h5Dir + 'game.html'] = "game.html";
# defaultCacheFiles[h5Dir + 'main.js'] = "main.js";
# defaultCacheFiles[h5Dir + 'project.json'] = "project.json";

i = 1
while i < len(sys.argv):
    p = sys.argv[i]
    if p.startswith("-"):
        p = p.replace("-","",1)
        params2[p] = sys.argv[i + 1]
        i = i + 2
    else:
        params1[p] = True
        i = i + 1
    if i > len(sys.argv):
        break

def getMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def findFiles():
    outStr="//this file is create auto by 'findFiles.py'"
    outStr+="\nvar g_resources = ["
    updateStr="";
    for parent,dirnames,filenames in os.walk(rootDir + params2["destDir"]):
    	for filename in filenames:
		if not (".DS_Store") in filename and not (".mp3") in filename and not (".ttf") in filename:
			file_ = os.path.join(parent,filename)
			if not ("\\src\\") in file_ and not ("/src/") in file_:
				md5 = getMd5(file_)
				file_ = file_[((file_.find('/',1))+1):]
				outStr += "\n\t\""+file_+"\","
				updateStr += "\n"+file_

    outStr += "\n];"
    outStr = outStr.replace(params2["ignoreRoot"],"")
    updateStr = updateStr.replace(params2["ignoreRoot"],"")
    return outStr,updateStr

def saveResources(outStr):
    output = open(rootDir + params2["exportDir"] + '/resource.js', 'wb')
    outStr=outStr.replace("\\","/")
    #outStr=outStr.replace("apple/git/moka-nn-client/","")
    #outStr=outStr.replace("MacData/git/moka-nn-client/","")
    #outStr=outStr.replace("build/dev_h5/","")
    output.write(outStr)
    output.close()

def saveCache(outStr):
    keys = defaultCacheFiles.keys()
    defaultCache = ""
    for i in range(len(keys)):
        key = keys[i]
        md5_ = getMd5(rootDir + key);
        defaultCache += "\n"+defaultCacheFiles[key]+"?v="+md5_
    output = open(rootDir + params2["h5Dir"] + '/cache.manifest', 'wb')
    version = time.strftime("%Y%m%d%H%M", time.localtime())
    tmp = "CACHE MANIFEST\n"
    tmp += "#v1.0." + version + "\n"
    tmp += "index.html" + "\n"
    tmp += "CACHE:\n"
    tmp += defaultCache
    tmp += outStr
    tmp += "\n\nNETWORK:\n"
    tmp += "*"
    tmp += "\n\nFALLBACK:\n\n"
    output.write(tmp)
    output.close()

outputStr,updateStr = findFiles();
saveResources(outputStr)

if not params1["noLog"]:
    print outputStr

print 'updateCache:' + str(params1["updateCache"])

if params1["updateCache"]:
	saveCache(updateStr)
	print updateStr

print 'all resources found!'



