#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Copyright: Deutsches Zentrum fuer Luft- und Raumfahrt e.V., 2015 (c)
Contact: daniel.boehnke@dlr.de and jonas.jepsen@dlr.de
'''
import os
import zipfile
import glob

class ZipFileExt(zipfile.ZipFile):
    EXCLUDE_LIST = set()
    def add_exclude(self, fileExtension):
        ZipFileExt.EXCLUDE_LIST.add(fileExtension)
    
    def remove_exclude(self, fileExtension):
        ZipFileExt.EXCLUDE_LIST.remove(fileExtension)
    
#     def check(self, filePath, globString):
#         '''
#         Checks if the file fits the given glob expression.
#         '''
#         pass

    def trimPath(self, filePath, rootPath):
        '''
        Removes the root path from the beginning of filePath.
        '''
        filePath = os.path.abspath(filePath)
        rootPath = os.path.abspath(rootPath)
        tmpList = os.path.abspath(filePath).split(os.path.sep)
        rootList = os.path.abspath(rootPath).split(os.path.sep)
        rootPathLength = len(rootList)
        return os.path.sep.join(tmpList[rootPathLength:])
    
    
#     def addByGlobString(self, dirPath, globStringList, baseDirName=None):
#         '''
#         Adds all contents described by the glob string to the zip file.
#         @param dirPath: describes the base path relative to which the files will be inserted.
#         '''
#         for globString in globStringList:
#             for filePath in glob.iglob(os.path.join(dirPath, globString)):
#                 basePath, fileName = os.path.split(filePath)
#                 pathInZip = self.trimPath(filePath, dirPath)
#                 if baseDirName:
#                     pathInZip = os.path.join(baseDirName, pathInZip)
#                 if os.path.isdir(filePath):
#                     print("DIR:", filePath)
#                 else:
#                     print("FILE:", filePath)
#                     #self.write(filePath, pathInZip)
    
    def addDirToZip(self, dirPath, baseDirName=None):
        '''
        Adds all contents of a directory recursively to an already opened zip file.
        '''
        for (basePath, dirNames, fileNames) in os.walk(dirPath):
            for fileName in fileNames:
                excluding = False
                for ext in ZipFileExt.EXCLUDE_LIST:
                    if fileName.endswith(ext):
                        excluding = True
                        break
                if excluding:
                    continue
                    
                filePath = os.path.join(basePath, fileName)
                pathInZip = self.trimPath(filePath, dirPath)
                if baseDirName:
                    pathInZip = os.path.join(baseDirName, pathInZip)
                self.write(filePath, pathInZip)
            if not fileNames and not dirNames:
                pathInZip = self.trimPath(basePath, dirPath)
                if baseDirName:
                    pathInZip = os.path.join(baseDirName, pathInZip)
                zipInfo = zipfile.ZipInfo(pathInZip + os.path.sep)
                #some web sites suggest doing
                #zipInfo.external_attr = 16
                #or
                #zipInfo.external_attr = 48
                #Here to allow for inserting an empty directory.  Still TBD/TODO.
                self.writestr(zipInfo, "")
    
    def addFileToZip(self, filePath):
        '''
        Adds a file to an already opened zip file.
        '''
        self.write(filePath)
        

def zipdir(dirPath, zipFilePath, baseDirName=None):
    '''
    Copies all contents of a directory recursively to a zip file.
    '''
    zipFile = ZipFileExt(zipFilePath, "w", zipfile.ZIP_DEFLATED)
    zipFile.addDirToZip(dirPath, baseDirName)
    zipFile.close()
        