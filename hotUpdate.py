import os
import os.path
import sys
import zipfile
import hashlib
import json
import datetime

nowGroup='1'
ch='1'
dateStr = datetime.datetime.now().strftime('%Y%m%d%H%M')
appVersion = '3'

if len(sys.argv) >= 2:
    ch=sys.argv[1]
    nowGroup=sys.argv[2]

version='1.0' + "." + nowGroup
rootDir="../"
updateDir=rootDir+"build_res/update/ch"+ch+"/"
zipFile = 'game_'+version+'.zip'

server_dirs={
    "1" : "http://moka-1253928017.file.myqcloud.com/ddz-client-update/ch1",
    "2" : "http://192.168.31.111:8080/git/ddz-client/update/ch2",
    "3" : "http://moka-1253928017.file.myqcloud.com/ddz-client-update/ch3"
}

allGroups={
}

allAssets={
}

def RestoreOldVersion():
    global allGroups
    global allAssets
    str = "{}"
    filename = updateDir + "groups.json"
    if os.path.exists(filename):
        reader = open(filename,'rb')
        str = reader.read()
    print "RestoreOldVersion: groups.json"
    print str
    allGroups = json.loads(str)

    str = "{}"
    filename = updateDir + "assets.json"
    if os.path.exists(filename):
        reader = open(filename,'rb')
        str = reader.read()
    print "RestoreOldVersion: assets.json"
    print str
    allAssets = json.loads(str)

def ChangeGameScriptVersion(filename_input,filename_output):
    print filename_input
    print filename_output
    fp = open(filename_output,'w')
    lines = open(filename_input).readlines()
    for s in lines:
        fp.write( s.replace('__VERSION__',dateStr).replace('APP_VERSION=1',"APP_VERSION="+appVersion))
    fp.close()

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b:
            break;
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def ZipGameRes():
    if os.path.exists(updateDir + zipFile):
        return
    azip = zipfile.ZipFile(updateDir + zipFile,'w')
    azip.write(updateDir + 'game.js','game.js',compress_type=zipfile.ZIP_DEFLATED)
    resDir = updateDir + 'res'
    pre_len = len(os.path.dirname(resDir))
    for parent, dirnames, filenames in os.walk(resDir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)
            azip.write(pathfile, arcname)
    azip.close()

def InsertNewVersion():
    global allGroups
    global allAssets

    md5Str = GetFileMd5(updateDir + zipFile)
    print json.dumps(allGroups)
    allGroups[nowGroup] = version
    print json.dumps(allGroups)
    allAssets["update"+nowGroup] = {
        "path" : zipFile,
        "md5" : md5Str,
        "compressed" : True,
        "group" : nowGroup
    }

def UpdateProjectManifest():
    reader = open(rootDir + "build_res/update/project.manifest",'rb')
    str = reader.read()

    str = str.replace('__VERSION__',version)
    str = str.replace('__GROUP_VERSIONS__',json.dumps(allGroups))
    str = str.replace('__UPDATE_ASSETS__',json.dumps(allAssets))
    str = str.replace('__SERVER_DIR__',server_dirs[ch])

    print "==================project.manifest=============="
    print str

    output = open(updateDir + "project.manifest", 'wb')
    output.write(str)
    output.close()

def UpdateVersionManifest():
    reader = open(rootDir + "build_res/update/version.manifest",'rb')
    str = reader.read()

    str = str.replace('__VERSION__',version)
    str = str.replace('__GROUP_VERSIONS__',json.dumps(allGroups))
    str = str.replace('__SERVER_DIR__',server_dirs[ch])

    print "==================version.manifest=============="
    print str

    output = open(updateDir + "version.manifest", 'wb')
    output.write(str)
    output.close()

def SaveNowVersion():
    output = open(updateDir + "groups.json", 'wb')
    output.write(json.dumps(allGroups))
    output.close()

    output = open(updateDir + "assets.json", 'wb')
    output.write(json.dumps(allAssets))
    output.close()   

RestoreOldVersion()

if allGroups.get(nowGroup):    
    print 'version ' + nowGroup + ' exists!'
else:
    ChangeGameScriptVersion(rootDir + "build/build_4_jsb/game.js",updateDir + "game.js")
    ZipGameRes()
    InsertNewVersion()
    UpdateProjectManifest()
    UpdateVersionManifest()
    SaveNowVersion()

print 'all done!'

