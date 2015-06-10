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
from ctypes import cdll, byref, CDLL, c_int, c_double, util
#todo: windll Handler is not available in Linux
import sys, os
from VAMPzero.Lib.Log.log import zeroLogger
from math import pi

log = zeroLogger('TIGL')

# open TIXI and TIGL shared libraries
if sys.platform == 'win32' or sys.platform =='win64':
    os.environ['PATH'] = os.path.dirname(sys.executable)+"\shared" + ';' + os.environ['PATH']
    log.debug("VAMPzero TIGL: Assuming this is windows")
    log.debug("VAMPzero TIGL: trying to load TIGL from sys.PATH")
    try:
        TIGL = cdll.TIGL
    except WindowsError, e:
        log.warning("VAMPzero TIGL: could not load TIGL from sys.PATH; %s" % e)
        try:
            from ctypes import windll
            TIGL = windll.LoadLibrary('TIGL.dll')
        except WindowsError, e:
            log.warning("VAMPzero TIGL: could not load TIGL from ./shared Folder; %s" % e)
            log.warning("VAMPzero TIGL: If working with CPACS this may lead to a crash")
            log.warning("VAMPzero TIGL: You can find TIGL at tigl.googlecode.com")
            try:
                tiglPath = util.find_library('TIGL.dll')
                TIGL = windll.LoadLibrary(tiglPath)
            except WindowsError, e:
                log.warning("VAMPzero TIGL: could not load TIGL from %s; %s" % (tiglPath, e))
else:
    log.debug("VAMPzero TIGL: Assuming this is linux")
    log.debug("VAMPzero TIGL: trying to load from /usr/local/lib/libTIGL.so")
    try:
        TIGL = CDLL("/usr/lib/i386-linux-gnu/libTIGL.so.2")
    except:
        log.warning("VAMPzero TIGL: Could not load TIGL")        
        log.warning("VAMPzero TIGL: If working with CPACS this may lead to a crash")
        log.warning("VAMPzero TIGL: You can find TIGL at tigl.googlecode.com")

#===========================================================================
#Functions 
#===========================================================================

def exportIGES(TIGLHandle, path):
    '''
    '''
    try:
        TIGL.tiglExportIGES(TIGLHandle,path)
    except:
        log.warning("VAMPzero TIGL: export to IGES did not work")

def openTIGL(TIXIHandle, modelUID):
    '''
    Opens an XML File specified by the modelUID and the TIXIHandle
    TIXI Handle must be given
    '''
    TIGLHandle = c_int(1)
    
    log.debug('VAMPzero TIGL: Trying to open TIGL')
    if modelUID is not None:
        try: 
            modelUID = str(modelUID)
        except:
            pass
        
        try:
            tiglReturn = TIGL.tiglOpenCPACSConfiguration(TIXIHandle, modelUID, byref(TIGLHandle))
        except WindowsError:
            #try with different handle
            try:
                TIGLHandle = c_int(2)
                tiglReturn = TIGL.tiglOpenCPACSConfiguration(TIXIHandle, modelUID, byref(TIGLHandle))
            except WindowsError:
                log.warning("VAMPzero TIGL: TIGL could not be loaded")
                tiglReturn = 0
    else:
        return None
    
    if tiglReturn:
        log.warning("VAMPzero TIGL: model could not be opened: %s" %modelUID)
        return None
    else:
        log.debug("VAMPzero TIGL: Opened %s in Handle %s" %(modelUID, TIXIHandle))
    
    
    return TIGLHandle

def getFuselageSegmentCount(TIGLHandle):
    '''
    mirrors the TIGL getFuselageSegmentCount
    '''
    segCount    = c_int(1)
    tiglReturn  = TIGL.tiglFuselageGetSegmentCount(TIGLHandle,1,byref(segCount))
    if tiglReturn:
        log.warning("VAMPzero TIGL: could not retrieve the number of segments")
    else:
        return segCount.value

def getFuselageDiameter(TIGLHandle, segmentIndex, eta):
    '''
    mirrors the TIGLfuselageGetCircumference method
    '''

    fuselageIndex = 1

    diameter = c_double(0.)

    tiglReturn = TIGL.tiglFuselageGetCircumference(TIGLHandle, fuselageIndex,segmentIndex, c_double(eta), byref(diameter))
    if tiglReturn:
        log.warning("VAMPzero TIGL: point could not be fetched!")

    return diameter.value/pi


def getFuselagePoint(TIGLHandle, segmentIndex, eta, angle):
    '''
    mirrors the TIGLfuselageGetPointAngle method
    '''
    
    fuselageIndex = 1
    
    xCoord = c_double(0.)
    yCoord = c_double(0.)
    zCoord = c_double(0.)
    
    tiglReturn = TIGL.tiglFuselageGetPoint(TIGLHandle, fuselageIndex,segmentIndex, c_double(eta), c_double(angle), byref(xCoord), byref(yCoord), byref(zCoord))
    if tiglReturn:
        log.warning("VAMPzero TIGL: point could not be fetched!")

    return xCoord.value, yCoord.value, zCoord.value


def getFuselageSurfaceArea(TIGLHandle,FuselageIndex):
    '''
    mirrors the TIGL getFuselageSurfaceArea method
    '''
    refArea     = c_double(0.)
    
    tiglReturn  = TIGL.tiglFuselageGetSurfaceArea(TIGLHandle,FuselageIndex,byref(refArea))
    
    if tiglReturn:
        log.warning("VAMPzero TIGL: could not retrieve the surfaceArea")

    else:
        return refArea.value

def getWingUpperPoint(TIGLHandle, wingIndex, segmentIndex, eta, ksi):
    '''
    mirrors the TIGLwingGetUpperPoint method
    '''
    if type(segmentIndex)== str:
        segmentIndex    = int(segmentIndex)
    
    xCoord = c_double(0.)
    yCoord = c_double(0.)
    zCoord = c_double(0.)
    
    tiglReturn = TIGL.tiglWingGetUpperPoint(TIGLHandle, wingIndex,segmentIndex, c_double(eta), c_double(ksi), byref(xCoord), byref(yCoord), byref(zCoord))
    if tiglReturn:
        log.warning("VAMPzero TIGL: point could not be fetched!")


    return xCoord.value, yCoord.value, zCoord.value

def getWingSurfaceArea(TIGLHandle,wingIndex):
    '''
    mirrors the TIGL getWingSurfaceArea method
    '''
    refArea     = c_double(0.)
    
    tiglReturn  = TIGL.tiglWingGetSurfaceArea(TIGLHandle,wingIndex,byref(refArea))
    
    if tiglReturn:
        log.warning("VAMPzero TIGL: could not retrieve the surfaceArea")
    else:
        return refArea.value
        

def getWingSegmentCount(TIGLHandle,wingIndex):
    '''
    mirrors the TIGL getWingSegmentCount
    '''
    segCount    = c_int(0)
    tiglReturn  = TIGL.tiglWingGetSegmentCount(TIGLHandle,wingIndex,byref(segCount))
    if tiglReturn:
        log.warning("VAMPzero TIGL: could not retrieve the number of segments")
    else:
        return segCount.value
