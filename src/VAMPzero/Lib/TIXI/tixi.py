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
from ctypes import cdll, byref, CDLL, c_int, c_char_p
import sys
import os

from VAMPzero.Lib.Log.log import zeroLogger
from VAMPzero.Lib.CPACS.general import evalList


# open TIXI and TIGL shared libraries

log = zeroLogger('TIXI')

 
if sys.platform == 'win32':
    os.environ['PATH'] = os.path.dirname(sys.executable)+"\shared" + ';' + os.environ['PATH']
    log.debug("VAMPzero TIXI: Assuming this is windows")
    log.debug("VAMPzero TIXI: trying to load TIXI from sys.PATH") 
    try: 
        TIXI = cdll.TIXI
    except WindowsError, e:
        print e
        log.warning("VAMPzero TIXI: could not load TIXI from sys.PATH")
        
        try:
            from ctypes import windll
            TIXI = windll.LoadLibrary('TIXI.dll')
        except WindowsError:
            log.warning("VAMPzero TIXI: could not load TIXI from ./shared Folder")
            log.warning("VAMPzero TIXI: If working with CPACS this may lead to a crash")
            log.warning("VAMPzero TIXI: You can find TIXI at tixi.googlecode.com")
    
    
else:
    log.debug("VAMPzero TIXI: Assuming this is linux")
    log.debug("VAMPzero TIXI: trying to load from /usr/local/lib/libTIXI.so")
    try: 
        TIXI = CDLL("/usr/lib/i386-linux-gnu/libTIXI.so.2")
    except:
        log.warning("VAMPzero TIXI: could not load TIXI from /usr/local/lib/libTIXI.so")
        log.warning("VAMPzero TIXI: If working with CPACS this may lead to a crash")
        log.warning("VAMPzero TIXI: You can find TIXI at tixi.googlecode.com")

#===============================================================================
# Functions
#===============================================================================

def openTIXI(path):
    '''
    Opens an XML File specified by Path Location for reading
    TIXI Handle must be given
    '''

    if type(path) != str:
        log.error("VAMPzero TIXI: path has no valid format: %s" % str(path))
        exit()#todo: enter error code here
    
    TIXIHandle = c_int(0)
    tixiReturn = TIXI.tixiOpenDocument(path, byref(TIXIHandle))
    
    if tixiReturn:
        log.warning("VAMPzero TIXI: document could not be opened %s" %path)
        return None
    else:
        log.debug("VAMPzero TIXI: Opened %s" %path)
    
    return TIXIHandle

def checkElement(tixiHandle,cpacsPath):
    '''
    mirrors tixiCheckElement
    '''

    tixiReturn      = TIXI.tixiCheckElement(tixiHandle,c_char_p(cpacsPath))

    if tixiReturn:
        log.debug("VAMPzero TIXI: element not found: %s" %cpacsPath)
        return False

    else:
        return True
    
def createXML(path):
    '''
    Creates an XML File specified by Path Location
    TIXI Handle must be given
    '''
    log = zeroLogger('TIXI')

    TIXIHandle = c_int(2)
    
    error = TIXI.tixiCreateDocument(path, byref(TIXIHandle))
    if error:
        log.warning("VAMPzero TIXI: document could not be created %s" %path)
   
    return TIXIHandle


def saveXML(path,TIXIHandle):
    '''
    Saves the XML document targeted by TIXI Handle to path location
    '''

    error = TIXI.tixiSaveDocument(TIXIHandle, path)
    if not error == 0:
        log.error('VAMPzero TIXI: could not save: %s'%path)



def closeXML(TIXIHandle):
    '''
    Closes the XML document targeted by the TIXI Handle
    !!! This does not save the document !!!
    '''
    error = TIXI.tixiCloseDocument(TIXIHandle)
    if not error == 0:
        log.error('VAMPzero TIXI: could not close TIXI Handle: %s'%TIXIHandle)
    else:
        log.debug('VAMPzero TIXI: closed TIXI Handle: %s'%TIXIHandle)

def getText(TIXIHandle, cpacsPath):
    '''
    Will get the text entry for a given XPATH
    '''
    
    text        = c_char_p()
    if checkElement(TIXIHandle, cpacsPath):
        error = TIXI.tixiGetTextElement(TIXIHandle,cpacsPath,byref(text))
        
        if error:
            log.info('VAMPzero TIXI: could not fetch text element from: %s' %cpacsPath)
            return None
        else:
            return text.value.strip()
        
def getList(TIXIHandle, cpacsPath):
    '''
    Tries to find semicolon separated list at the specified cpacsPath. Then will try to return a list object
    with evaluated entries
    '''
    #first check the path  
    if checkElement(TIXIHandle,cpacsPath):
        line = getText(TIXIHandle,cpacsPath)

        if line.find(';') != -1:
            list    = evalList(line.strip().split(';'))
        else: 
            list    = eval(line.strip())
        
        return list
            
    else:
        log.warning("VAMPzero TIXI: Could not find the specified path: %s"%cpacsPath)
        return None 
        
def getLastIndex(TIXIHandle, path, element):
    '''
    This function finds the last index of an element in path.
    It is equivalent to the number of elements with name $element in path.
    '''
    index = 1
    while True:
        if not checkElement(TIXIHandle,path + "/" + element + "["+str(index) + "]"):
            return index-1
        index += 1

def setText(TIXIHandle, cpacsPath, value):
    '''
    Sets the element at cpacsPath to the given value.
    If the element doesn't exist it will be created.
    '''

    try:
        found = checkElement(TIXIHandle,cpacsPath)
        if not found:
            log.info('VAMPzero TIXI: %s element not found => creating it' %cpacsPath)
            buildTree(TIXIHandle, cpacsPath)
            addText(TIXIHandle, cpacsPath, value,format)
        else:
            log.info('VAMPzero TIXI: %s element found => updating it' %cpacsPath)
            TIXI.tixiUpdateTextElement(TIXIHandle,cpacsPath,str(value))
    except:
        pass

def addDouble(TIXIHandle,cpacsPath,result,format= None):
    '''
    Adds a double Value (result) to the element at cpacsPath
    '''
    try:
        path, element = splitXPath(cpacsPath)
        error = TIXI.tixiAddDoubleElement(TIXIHandle, path,element,result,format)
        if not error:
            log.info('VAMPzero TIXI: %s/%s in ToolOutput.xml: %s' %(path,element,str(result.value)))
        else:
            log.info('VAMPzero TIXI: %s/%s error while parsing to file'%(path,element))
            log.info('VAMPzero TIXI: %s/%s starting build up loop again'%(path,element))
            #@note: will lead to the feared death of too many XML elements, if a different error pops up
            buildTree(TIXIHandle, cpacsPath)
            addDouble(TIXIHandle, cpacsPath, result,format)

    except:
        pass

def addText(TIXIHandle,cpacsPath,result,format= None):
    '''
    Adds a text Value (result) to the element at cpacsPath
    '''
                        
    try:
        path, element = splitXPath(cpacsPath)
        error = TIXI.tixiAddTextElement(TIXIHandle, path,element,str(result))
        if not error:
            log.info('VAMPzero TIXI: %s/%s in ToolOutput.xml: %s' %(path,element,str(result.value)))
        else:
            log.info('VAMPzero TIXI: %s/%s error while parsing to file'%(path,element))
            log.info('VAMPzero TIXI: %s/%s starting build up loop again'%(path,element))
            #@note: will lead to the feared death of too many XML elements, if a different error pops up
            buildTree(TIXIHandle, cpacsPath)
            addText(TIXIHandle, cpacsPath, result,format)

    except Exception, e:
        pass
        

def createElement(TIXIHandle,path, element):
    '''
    Creates a new element described by a path and element name within the document targeted by the TIXIHandle
    '''
    
    error = TIXI.tixiCreateElement(TIXIHandle, path, element)
    if not error:
        log.info('VAMPzero TIXI: created %s' %(path+element))
    else: 
        log.info('VAMPzero TIXI: could not create %s' %(path+element)) 
    
def splitXPath(cpacsPath):
    '''
    Splits a cpacsPath String into a path and a element 
    Example 
    cpacsPath = /model/global/Mass results in 
    path = /model/global
    element = Mass
    '''
    cpacsPath = cpacsPath.split('/')
    path      = ''
    
    for item in cpacsPath: 
        if item != cpacsPath[len(cpacsPath)-1]:
            if item != '':
                path = path + '/' + item
        else:
            element = item
        
    return path,element
 


def buildTree(TIXIHandle,cpacsPath):
    '''
    Creates tree for a given XPath
    As add double Element Function in TIXI requires existing parent elements
    this function will build up the whole tree. 
    still in preliminary status, probably buggy 
    Example:
    Input: cpacsPath = /model/fuselage/global/length
    
    loop:
    check if /model exists
    if true create model
    end loop do the same with model/global
    
    length element will be skipped!!!
    '''

    
    split     = cpacsPath.split('/')
    path      = ''
    #Pop last element, as it will only be handled by addDouble Element
    split.pop()
    
    for item in split:
        if item != '' and path != '' and TIXI.tixiCheckElement(TIXIHandle,path+'/'+item)==8:
            try:
#                #@note: TIXI buildtree is the replacement here a smart move?
#                #@todo: replacement should include more values (i.e.[53]) for points in pointlist
#                item = item.replace('[1]','')
#                item = item.replace('[2]','')
#                item = item.replace('[3]','')
#                item = item.replace('[last()]','')
                specifierIndex = item.find('[')
                #@note: maybe this is a better way since it allows for different kinds of specifiers (i.e. [name="wing"]) for toolspecific components
                if specifierIndex != -1:
                    item = item[:specifierIndex]
                error = TIXI.tixiCreateElement( TIXIHandle, path,item , 0 )
                if not error:
                    log.info('VAMPzero TIXI: %s/%s created' %(path,item))
                    # set item path to the last item
                    # this is needed when a new node with the same name as an existing one is created
                    # i.e. components/component[name="wing"]/disciplines/discipline[name="geometry"]/parameters/parameter[name="taperRatio"]
                    item = item + '[last()]'
                                    
            except:
                log.warning('VAMPzero TIXI: %s/%s could not be created') %(path,item)
                    
        path = path +'/' + item
        path = path.replace('//', '/')
    
    def merge(cpacsIn,cpacsOut):
        '''
        This Routine will merge the values from cpacsOut into cpacsIn
        '''
        pass

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
