#!/usr/bin/python
#coding=utf-8


import os
import sys
import shutil
import json
import re
import platform
import xml.etree.ElementTree as ET
import subprocess
#from subprocess import call

reload(sys)
sys.setdefaultencoding("utf-8")


CURRENT_DIR=os.path.dirname(os.path.realpath(sys.argv[0]))
JS_LISTPATH=os.path.join(CURRENT_DIR,"..","src","jsList.js")
EXPORT_ANT_FILE=os.path.join(CURRENT_DIR,"build_concat.xml")
                    

class AntXMLbuilder():
    _fileContent=""
    _exportAntFile=EXPORT_ANT_FILE
    _isOpenUsedResources=False
    
    def __init__(self):
        print "AntXMLbuilder init=======>>>"

    def startWork(self):
        self._fileContent='<?xml version="1.0" encoding="UTF-8"?>\n'
        self._fileContent+='<project name="buildconcat" default="concatjs">\n'
        self._fileContent+='    <property name="charset" value="utf-8"/>\n'
        self._fileContent+='    <property name="projDir" value="${ant.file.buildconcat}/../../"/>\n'
        self._fileContent+='    <target name="concatjs">\n'
        self._fileContent+='        <property name="src" value="${destDir}/src"/>\n'
        self._fileContent+='        <concat destfile="${destDir}/tmp.js" encoding="${charset}" outputencoding="${charset}">\n'
        self._fileContent+='            <path path="${src}/package.js"/>'
        
        self._fileObject = open(self._exportAntFile, 'w')
        self._isOpenUsedResources=False


    def isUsedResources(self,line):
        findIndex=line.find('var jsList = [');
        if findIndex>=0:
            return True
        return False

    def parseUsedResources(self,line):
        findIndex=line.find('];')
        if findIndex>=0:
            self._isOpenUsedResources=False
        else:
            findIndex=line.find('"src')
            if findIndex>=0:
                endIndex=line.find(',')
                newLine='            <path path="${src}'+line[findIndex+4:endIndex]+'/>\n'
                self.pushLine(newLine)
                findIndex=line.find('/config.js')
                if findIndex>=0:
                    newLine='            <path path="${src}/ch_info.js"/>\n'
                    self.pushLine(newLine)
            else:
                self.pushLine('\n')

    def checkLine(self,line):

        if self._isOpenUsedResources:
            self.parseUsedResources(line)
            return

        if self.isUsedResources(line):
            self._isOpenUsedResources=True



    def pushLine(self,line):
        self._fileContent=self._fileContent+line

    def finishWork(self):
        self._fileContent+='        </concat>\n'
        self._fileContent+='    </target>\n'
        self._fileContent+='</project>\n'
        self._fileObject.write(self._fileContent)
        self._fileContent=""
        self._fileObject.close()



class AntXMLMaker():
    
    _antXMLbuilder=""

    def __init__(self):
        self._antXMLbuilder=AntXMLbuilder()
        print "AntXMLMaker init=======>>>"

    def parseUiJson(self):
        jsonFilePath=JS_LISTPATH
        uiJsonRebuilder=self._antXMLbuilder
        uiJsonRebuilder.startWork()
        fileObject=open(jsonFilePath,"rb")
        for line in fileObject:
            uiJsonRebuilder.checkLine(line)
        
        uiJsonRebuilder.finishWork()

    def doWork(self):
        self.parseUiJson()

        print "AntXMLMaker doWork=======>>>"



if __name__ == '__main__':
    
    pngCollector = AntXMLMaker()
    pngCollector.doWork()

    print "\nAll OK"



