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
import sys
import os
import shutil
from VAMPzero import version as VAMPversion
import argparse
from VAMPzero.Lib.Utilities import zipdir
import zipfile


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    # to be able to use main() in interactive mode
    if argv is None:
        argv = sys.argv
    try:
        try:
            usage = "usage: %prog [options] arg1 arg2\n\ttype '%prog --help' for help"
            parser = argparse.ArgumentParser(description='Build VAMPzero')
            parser.add_argument("--doc", help="creating VAMPzeros documentation", action='store_true')
            parser.add_argument("--exe", help="compiling VAMPzero to executable", action='store_true')
            parser.add_argument("--win32", help="creating a zipfile containing the win32 binary package", action='store_true')
            parser.add_argument("--win64", help="creating a zipfile containing the win64 binary package", action='store_true')
            parser.add_argument("--src", help="creating a zipfile containing VAMPzeros source code", action='store_true')
            parser.add_argument("--all", help="do the complete build process", action='store_true')
            parser.add_argument("--clean", help="removes all temporary build files", action='store_true')
            parser.add_argument("--test", help="perform tests for VAMPzero", action='store_true')
            parser.add_argument("--removeDoublesFromBin", help="removes all files in bin which are also produced by py2exe", action='store_true')
            args = parser.parse_args()
            
            if args.all:
                make_all()
            else:
                '''
                The order of the following arguments is important
                since some functions rely on the output of others.
                '''
                if args.test:
                    run_tests()
                if args.clean:
                    clean()
                if args.doc:
                    make_doc_html()
                    zip_doc()
                if args.exe or args.win32 or args.win64:
                    make_exe()
                if args.removeDoublesFromBin:
                    removeDoublesfromBin()
                if args.win32 or args.win64:
                    make_bin()
                if args.win32:
                    make_bin_win32()
                if args.win64:
                    make_bin_win64()
                if args.src:
                    make_src()
        except (Exception), msg:
            raise Usage(msg)

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2


PATH_TO_TOP = ".."
CWD = os.getcwd()
ZIPNAME_COMPLETE = "../VAMPzero" + VAMPversion + "bin-complete.zip"

def run_tests():
    path = os.path.split(os.path.abspath(__file__))[0]
    os.system("python {}".format(os.path.join(path, '../test/run_tests.py')))

def make_doc_html():
    '''
    Calculates script to calculate sensitivities for VAMPzeros parameters.
    Create VAMPzero documentation in html format using Sphinx's make process.
    '''
    print("Creating documentation via sphinx...")
    path_to_doc = "VAMPzero/doc"
    try:
        os.system("python VAMPzeroDoc.py")
        os.chdir(path_to_doc)
        os.system("make html")
    finally:
        os.chdir(CWD)

def zip_doc():
    '''
    Compresses VAMPzeros documentation into a zip file.
    This function does not update the documentation and therefore needs make_doc_html to run up-front.
    An existing zip file will be deleted.
    This function uses pure python code to work on different OS.
    '''
    print("Creating documenation zip file...")
    path_to_html = "VAMPzero/doc/_build/html"
    try:
        zipname = PATH_TO_TOP + "/VAMPzero" + VAMPversion + "Doc_html.zip"
        zipdir.zipdir(path_to_html, zipname)
    finally:
        os.chdir(CWD)

def make_exe():
    '''
    Creates VAMPzeros binary by using the py2exe setup script.
    '''
    print("Executing py2exe ...")
    os.system("python setup_py2exe.py py2exe")

def make_bin():
    '''
    Creates a zip file with all files for binary distribution.
    Including 32bit and 64bit versions of files.
    Needs compiled binaries as created by make_exe().
    '''
    print("Creating binary zip file...")
    try:
        zipFile = zipdir.ZipFileExt(ZIPNAME_COMPLETE, "w", zipfile.ZIP_DEFLATED)
        # get prepared files
        zipFile.addDirToZip('../bin')
        # get compiled files
        zipFile.addDirToZip('../src/bin')
        # add mapping files
        zipFile.addFileToZip('mappingInputRaw.xsl')
        zipFile.addFileToZip('mappingOutput.xml')
        zipFile.close()
    except Exception as e:
        print("Error while building bin:", e)
    finally:
        os.chdir(CWD)

def make_bin_win32():
    '''
    Creates a zip file of VAMPzeros win32 binary.
    Needs compiled binaries as created by make_exe().
    '''
    print("Creating win32 zip file...")
    try:
        zipname = PATH_TO_TOP + "/VAMPzero" + VAMPversion + "bin-win32.zip"
        zin = zipdir.ZipFileExt(ZIPNAME_COMPLETE, 'r')
        zout = zipdir.ZipFileExt(zipname, 'w')
        for item in zin.infolist():
            myBuffer = zin.read(item.filename)
            print item.filename
            if item.filename.endswith('vampzerostandalone_64.jar'):
                continue
            else:
                zout.writestr(item, myBuffer)
        zout.close()
        zin.close()
    except Exception as e:
        print("Error while building win32:", e)
    finally:
        os.chdir(CWD)

def make_bin_win64():
    '''
    Creates a zip file of VAMPzeros win32 binary.
    Needs compiled binaries as created by make_exe().
    '''
    print("Creating win64 zip file...")
    try:
        zipname = PATH_TO_TOP + "/VAMPzero" + VAMPversion + "bin-win64.zip"
        zin = zipdir.ZipFileExt(ZIPNAME_COMPLETE, 'r')
        zout = zipdir.ZipFileExt(zipname, 'w')
        for item in zin.infolist():
            myBuffer = zin.read(item.filename)
            print item.filename
            if item.filename.endswith('vampzerostandalone_64.jar'):
                continue
            else:
                zout.writestr(item, myBuffer)
        zout.close()
        zin.close()
    except Exception as e:
        print("Error while building win64:", e)
    finally:
        os.chdir(CWD)

def make_src():
    '''
    Creates a zip file of the source code version of VAMPzero.
    '''
    print("Creating source zip file...")
    includeFiles = ['setup.py',
                    'README.txt',
                    'NOTICE',
                    'VAMPzero.ico',
                    'VAMPzero.jpg',
                    'VAMPzero.py',
                    'VAMPzeroCPACS.py',
                    'VAMPzeroDoc.py',
                    'mappingInputRaw.xsl',
                    'mappingOutput.xml',
                    'ToolInput/toolInput.xml']
    
    emptyDirs = ['ToolOutput',
                 'ReturnDirectory']
    try:
        zipname = "../VAMPzero" + VAMPversion + "src.zip"
        zipout = zipdir.ZipFileExt(zipname, 'w')
        zipout.add_exclude('.pyc')
        zipout.addDirToZip('./VAMPzero', "VAMPzero")
        for filePath in includeFiles:
            zipout.write(filePath, filePath)
        for emptyDir in emptyDirs:
            zipInfo = zipfile.ZipInfo(emptyDir + os.path.sep)
            zipout.writestr(zipInfo, "")
        zipout.close()
#         os.system("touch ../" + zipname)
#         os.system("rm ../" + zipname)
#         # get compiled files
#         # exclude all files in bin, build, and all *.pyc files in top directory and subdirs
#         os.system("zip -r ../" + zipname + " * -x bin/\* build/\* \*/\*.pyc \*.pyc")
    finally:
        os.chdir(CWD)

def clean():
    '''
    A function to clean VAMPzero from all temp files of the build process.
    This includes .pyc files, the src/bin directory as well as the created html doc.
    '''
    # make sure the current directory is the right one
    # otherwise the wrong stuff could be deleted
    path = os.path.split(os.path.abspath(__file__))[0]
    binPath = os.path.join(path, 'bin')
    buildPath = os.path.join(path, 'build')
    if os.path.exists(binPath) and os.path.exists(buildPath):
        print("Removing {}".format(binPath))
        shutil.rmtree(binPath)
        print("Removing {}".format(buildPath))
        shutil.rmtree(buildPath)

def make_all():
    '''
    Starts the complete build process.
    '''
    #clean()
    make_doc_html()
    zip_doc()
    make_exe()
    make_bin_win32()
    make_bin_win64()
    make_src()


def removeDoublesfromBin():
    path = os.path.split(os.path.abspath(__file__))[0]
    binDirUpper = os.path.join(path, '../bin')
    binDirLower = os.path.join(path, 'bin')
    
    def trimPath(filePath, rootPath):
        '''
        Removes the root path from the beginning of filePath.
        '''
        filePath = os.path.abspath(filePath)
        rootPath = os.path.abspath(rootPath)
        tmpList = os.path.abspath(filePath).split(os.path.sep)
        rootList = os.path.abspath(rootPath).split(os.path.sep)
        rootPathLength = len(rootList)
        return os.path.sep.join(tmpList[rootPathLength:])
    print("Removing redundant files...")
    upperList =  []
    for (dirpath, dirnames, filenames) in os.walk(binDirUpper):
        for filename in filenames:
            upperList.append(trimPath(os.path.join(dirpath, filename), binDirUpper))
    
    lowerList =  []
    for (dirpath, dirnames, filenames) in os.walk(binDirLower):
        for filename in filenames:
            lowerList.append(trimPath(os.path.join(dirpath, filename), binDirLower))
    
    removeList = []
    for item in upperList:
        if item in lowerList:
            removeList.append(os.path.abspath(os.path.join(binDirUpper, item)))
    
    for item in removeList:
        print("removing: {}".format(item))
        os.remove(item)
        
    # remove empty directories
    emptyDirsList = []
    for (dirpath, dirnames, filenames) in os.walk(binDirUpper):
        if not filenames and not dirnames:
            emptyDirsList.append(dirpath)
    
    for item in emptyDirsList:
        print("removing empty dir: {}".format(item))
        os.removedirs(item)

if __name__ == "__main__":
    sys.exit(main())
