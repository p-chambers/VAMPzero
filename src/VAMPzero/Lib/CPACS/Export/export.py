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

from math import cos, pi
from os import remove
from types import ListType
import re

from lxml.etree import Element as lxmlElement

from VAMPzero.Lib.CPACS.cpacs import doubleBaseType, pointType, pointAbsRelType, \
    transformationType, stringBaseType, positioningType, parse, pointListType, \
    profileGeometryType
from VAMPzero.Lib.Log.log import zeroLogger
import VAMPzero.Lib.TIXI.tixi as tixiLib


def cpacsExport(component, path = '.\\cpacs.xml'):
    '''
    This function exports the given component to the file given by the path parameter.
    @author: Jonas Jepsen
    @param component: component for export
    @param path: path to export file
    '''
    log           = zeroLogger('cpacsExport')
    log.info('')
    log.info("##############################################################################")
    log.info("VAMPzero CPACS Export to %s" %(path))
    log.info("##############################################################################")
    
    #reset outfile
    try: 
        remove(path)
    except:
        pass
    outfile = open(path,'w')
    outfile.writelines(['<cpacs></cpacs>'])
    outfile.close()
    
    # pars CPACS export file
    CPACSObj     = parse(path)

    component.cpacsExport(CPACSObj)

    outfile = open(path,'w')
    #outfile.write('<?xml version="1.0" encoding="UTF-8"?>'+"\n")
    
    CPACSObj.export(outfile,0)
    outfile.close()

    log.info("VAMPzero CPACS EXPORT: done.")

def resultExport(component, path, componentWise=True):
    '''
    This function exports the given component to the file given by the path parameter.
    @author: Jonas Jepsen
    @param component: component for export
    @param path: path to export file
    '''
    log           = zeroLogger('resultExport')
    log.info('')
    log.info("##############################################################################")
    log.info("VAMPzero Result Export to %s" %(path))
    log.info("##############################################################################")
    
    #reset outfile
    try: 
        remove(path)
    except:
        pass

    outfile = open(path, 'w')
    for para in component.getParameters(componentWise):
        if hasattr(para,'resultExport'): # check should not be necessary 
            para.resultExport(outfile)
    
    outfile.close()

    log.info("VAMPzero RESULT EXPORT: done.")

def resultToolspecExport(component, path):
    '''
    Exports marked parameters into VAMPzeros toolspecific results node.
    @param component: should be the aircraft component
    '''
    log           = zeroLogger('resultToolspecExport')
    log.info('')
    log.info("##############################################################################")
    log.info("VAMPzero Result Toolspecific Export to %s" %(path))
    log.info("##############################################################################")
    #reset outfile
    
    TIXIHandle      = tixiLib.openTIXI(path)
    
    for para in component.getParameters():
        if not para['exportTS']:
            continue
        # try to get componentNode
        compPathBase = '/cpacs/toolspecific/vampZero/results/components/component'
        compPath = compPathBase + '[name="%s"]' % para.parent.id
        discPathBase = compPath + '/disciplines/discipline'
        discPath = discPathBase + '[name="%s"]' % para["discipline"]
        paraPathBase = discPath + '/parameters/parameter'
        paraPath = paraPathBase + '[name="%s"]' % para.getName()
        # try to get component node
        exists = tixiLib.checkElement(TIXIHandle, compPath)
        if not exists: # create it
            tixiLib.buildTree(TIXIHandle, compPath + '/name')
            tixiLib.addText(TIXIHandle, compPathBase + '[last()]/name', para.parent.id)
        # try to get discipline node
        exists = tixiLib.checkElement(TIXIHandle, discPath)
        if not exists: # create it
            tixiLib.buildTree(TIXIHandle, discPath + '/name')
            tixiLib.addText(TIXIHandle, discPathBase + '[last()]/name', para["discipline"])
        # try to get parameter node
        exists = tixiLib.checkElement(TIXIHandle, paraPath)
        if not exists: # create it
            tixiLib.buildTree(TIXIHandle, paraPath + '/name')
            tixiLib.addText(TIXIHandle, paraPathBase + '[last()]/name', para.getName())
        tixiLib.setText(TIXIHandle, paraPath + '/value', para.getValue())
    
    tixiLib.saveXML(path, TIXIHandle)
    tixiLib.closeXML(TIXIHandle)

    log.info("VAMPzero RESULT TOOLSPECIFIC EXPORT: done.")

def buildElement(Obj,el,uID=''):
    '''
    This function builds an attribute object with the given name $el.
    If the element has a uID it will be set to the passed value.
    
    **VAMPzero 0.3**
    Inserted a second node here, as the new version(2.4c) of generateDS seems to generate a buildChildren function
    that heavily relies on the value
    Daniel 

    @author: Jonas Jepsen
    @param Obj: object where the element will be created
    @param el: name of the element/attribute
    @param uID: the uID of the element
    @return: returns the created element 
    '''
    # create node
    node = lxmlElement(el)
    #print "START ","#"*75
    #print "element: ", el
    #print "node: ", node
    #
    Obj.buildChildren(node,node,el)
    if el == 'global':
        ret_Obj = getattr(Obj, 'global_')
    else:
        ret_Obj = getattr(Obj, el)
    if isinstance(ret_Obj, ListType):
        # if Obj is a List use created Element (the last one)
        ret_Obj = ret_Obj[-1]
    # if object has the attribute uID -> create it
    if hasattr(ret_Obj, 'uID'):
        #print el,"has attr uID", ret_Obj
        ret_Obj.uID = uID
    else:
        pass#print el,"has NO attr uID", ret_Obj
    #print "ret_Obj: ", ret_Obj
    #print "ENDE ", "#"*75
    #if hasattr(ret_Obj,"uID"):
    #    print "new element created with uID:",ret_Obj, ret_Obj.get_uID()
    #else:
    #    print "new element created:",ret_Obj
    #print ret_Obj.__dict__
    return ret_Obj


def evalUID(el):
    '''
    this function evaluates the uID_part of an element
    In other words; it splits the uID and the element name where possible.
    (example 'wing[htp]'returns 'htp', 'wing')
    @author: Jonas Jepsen
    @param el: xpath-element (like 'wing[htp]')
    @return: index, el (like 'htp','wing' )
    @note: this function works with uIDs that contain alphanumeric characters or an underscore [a-zA-Z0-9_]
    '''
    # default uID if no name is given in path
    uid = ''
    # get uID from xPath element
    # \w : matches any alphanumeric character and the underscore; this is equivalent to the set [a-zA-Z0-9_]
    # in total the expression is looking for  a opening bracket '[' and takes all alphanumeric characters that follow as the uID.
    # this works, because it stops at the closing bracket ']' which is not an alphanumeric character.
    # check http://docs.python.org/library/re.html for further informations about the expression (?<= )
    m = re.search('(?<=\[)\w+',el)
    if m is not None:
        # get the matching expression for the uID
        uid = m.group(0)
        # see http://docs.python.org/library/re.html for an explanation of the group-method
        el = el.replace('['+uid+']','') # remove the [uID] from the cpacs-path expression; e.g. wing[htp] => wing
    return uid, el


def getObjfromXpath(CPACSObj,xpath):
    '''
    This function gets the CPACSObject to a certain xpath.
    If no uID is given, it gets the first element at xpath.
    @author: Jonas Jepsen
    @param CPACSObj: the CPACSObject 
    @param xpath: the xpath of the wanted object.
    @return: the found Object at xpath in CPACSObj
    '''
    ############################################
    #### START getObjfromXpath subfunctions ####
    ############################################
    #################################
    # The following 4 functions process list elements
    # 1. getByUID()    - gets the element with the given uID
    # 2. getByIndex()  - gets the element with the given index
    # 3. getNew()      - gets a new element wich is appended to the end of the list
    # 4. getFirst()    - gets the first element of the list
    #################################
    def getByUID(Obj,lastObj,el,uID):
        '''
        This function finds the element with the given uID in the given list.
        If it can't find an element with the right uID a new element with the given uID will be created and appended to the list.
        @author: Jonas Jepsen
        @param Obj: the list of elements (el)
        @param lastObj: the Object which is parent to the list.
        @param el: the "code" of the element (is used to identify the type of the element).
        @param uID: the uID of the wanted element.
        @return: the wanted object
        '''
        # --------------------------------
        # START PROCESS ELEMENT WITH UID ATTRIBUTE
        # --------------------------------
        # init a variable if the element with the right uID was found
        found = False
        for i in range(len(Obj)):   # search through the whole object until the element belonging to the given uID is found
            try:
                #print "with UID:",Obj[i],Obj[i].get_uID()
                if Obj[i].get_uID()==uID:
                    #print "element found!", Obj[i], Obj[i].get_uID(), len(Obj)
                    Obj =  Obj[i]
                    found = True
                    break
            except AttributeError:
                print "noUID available"
                print "If you see this, there is something wrong with the getObjfromXpath-function!!!"
        if not found:
            # print "element NOT found! => creating it"
            Obj = buildElement(lastObj,el, uID)
            #print Obj, "created"
        # --------------------------------
        # END PROCESS ELEMENT WITH UID ATTRIBUTE
        # --------------------------------
        return Obj
    
    def getByIndex(Obj,lastObj,el,numUID):
        '''
        This function gets the object to an element by a given index FROM A LIST of objects.
        If the index exceeds the list entries new elements up to the needed index will be created.
        @author: Jonas Jepsen
        @param Obj: the list of elements (el)
        @param lastObj: the Object which is parent to the list.
        @param el: the "code" of the element (is used to identify the type of the element).
        @param numUID: element index
        @return: the wanted object
        '''
        # --------------------------------
        # START GET BY INDEX
        # --------------------------------
        #if the element has no uID attribute it is assumed to be a numbered list
        # the uID is therefore assumed to be an integer
        #print "no uID attribute found in :",Obj[0]
        try:
            if cmp(numUID,len(Obj))<=0:
                #print "without UID:",Obj[numUID-1]
                Obj = Obj[numUID-1]
            else:
                #print "WARNING: an element was appended because the index is out of bound!!"
                #print "creating empty (None) elements to fit the index."
                diff    = numUID-1-len(Obj)
                #print "length of Obj=" + str(len(Obj))
                #print "numUID=" + str(numUID)
                #print "adding", diff, "None elements"
                for i in range(diff):
                    #print "adding None element"
                    #Obj.append(None)
                    buildElement(lastObj, el) # BEWARE, this call changes Obj!!! Because lastObj is parent to Obj
                #print("length of Obj=" + str(len(Obj)))
                # the index of the uID is out of bound.
                # a new element will be created and added to the list.
                # since the element has no uID only two parameters are given for buildElement()
                #print Obj
                buildElement(lastObj, el) # BEWARE, this call changes Obj!!! Because lastObj is parent to Obj
                #print Obj
                #print("length of Obj=" + str(len(Obj)))
                # check if the index of the created element equals uID
                if cmp(numUID,len(Obj))!=0:
                    print "WARNING: the index of the added element (", Obj[len(Obj)-1],") is", len(Obj),"which differs from the given index (uID)", uID_part
                # make the new Object the chosen/created element (for next iteration step)
                Obj = Obj[len(Obj)-1]
                    
        except IndexError:
            print "Accessing element via uID failed. Index out of bound!" 
        return Obj
        # --------------------------------
        # END GET BY INDEX
        # --------------------------------
    
    def getNew(Obj,lastObj,el,uID=''):
        '''
        This function creates a new element in an empty list.
        At this stage it does not matter whether the element has a uID attribute,
        because that is covered in the buildElement-function.
        @author: Jonas Jepsen
        @param Obj: the list of elements (el)
        @param lastObj: the Object which is parent to the list.
        @param el: the "code" of the element (is used to identify the type of the element).
        @param uID: the uID of the wanted element.
        @return: the wanted object
        '''
        # --------------------------------
        # START GET NEW
        # --------------------------------
        buildElement(lastObj,el, uID)
        Obj = Obj[len(Obj)-1]
        
        if not hasattr(Obj,'uID'):
            #print "New element (", Obj, ") without uID attribute created."
            #print "The given index was ", uID_part
            #print "empty element no uID:",Obj
            pass
        else:
            #print "empty element:",Obj, Obj.get_uID()
            pass
        # --------------------------------
        # END GET NEW
        # --------------------------------
        return Obj
    
    def getFirst(Obj,lastObj,el,uID=''):
        '''
        This function gets the first element of a list.
        If the list is empty a new element is created.
        @author: Jonas Jepsen
        @param Obj: the list of elements (el)
        @param lastObj: the Object which is parent to the list.
        @param el: the "code" of the element (is used to identify the type of the element).
        @param uID: the uID of the wanted element.
        @return: the wanted object
        '''
        # --------------------------------
        # START GET FIRST
        # --------------------------------
        if len(Obj)==0:
            buildElement(lastObj,el, uID)
        Obj = Obj[0]
        # --------------------------------
        # END GET FIRST
        # --------------------------------
        return Obj

    ##########################################
    #### END getObjfromXpath subfunctions ####
    ##########################################
    
    #@note: this function depends on the cpacslib, changes might be necessary
    # split the xpath into single tree elements
    split = xpath.split('/')
    #print "\t split: ", split
    Obj = CPACSObj
    lastObj = Obj
    #print "begin split"
    # split xpath
    for el in split:
        # evaluate the xpath element to retrieve the uID
        uID, el = evalUID(el)
        # continue with next step if the current element is empty or cpacs    
        if el == '' or el =='cpacs':
            continue
        # change special element names for the cpacslib.
        if el == 'global':  # fix name, automatic change in cpacslib out of keyword issues
            el = 'global_'
        
        # check if the object has the needed element
        # if NOT print FAILURE and exit
        # otherwise get element
        if not hasattr(Obj, el):
            print "FAILURE: element", Obj, "has no attribute", el,xpath
            print "Check CPACS documentation, or update schema and cpacslib"
            exit(0)
        else:
            # save last object for 'buildElement'
            lastObj = Obj
            # make the element the new object
            Obj = getattr(Obj, el)
            if Obj is None:
                #print "IS None!"
                # process special elements for cpacslib
                if el == 'global_':
                    Obj = buildElement(lastObj,'global',uID)
                else:
                    Obj = buildElement(lastObj,el, uID)

            # check if instance is a list
            elif isinstance(Obj, ListType):
                # --------------------------------
                # START PROCESS LIST ELEMENTS
                # --------------------------------
                #print "IS LIST"
                try:
                    if uID == '':
                        # append new element to list
                        Obj = getFirst(Obj,lastObj,el,uID)
                        pass
                    else:
                        numUID = int(uID)
                        Obj = getByIndex(Obj,lastObj,el,numUID)
                except:
                    # find element with uID
                    Obj = getByUID(Obj,lastObj,el,uID)
                
                # --------------------------------
                # END PROCESS LIST ELEMENTS
                # --------------------------------
            else:
                #print "INFO: basic type found :",Obj
                pass
    #print "end split"
    return Obj

    

def createHeader(myWing, id):
    '''
    this function creates the header information in myWing
    @author: Jonas Jepsen
    @param myWing: CPACS wing object
    @param id: the wings id
    @return: strUID, the uID (in string form) of the wing
    '''
    strUID       = myWing.get_uID()
    myUID        = strUID
    myName       = stringBaseType(None,None,None,id)
    myDescr      = stringBaseType(None,None,None,strUID)
    myWing.set_uID(myUID)
    myWing.set_name(myName)
    myWing.set_description(myDescr)
    return strUID

def createTransformation(parent, refType='absGlobal',tx=0.,ty=0.,tz=0., sx=1.,sy=1.,sz=1., rx=0.,ry=0.,rz=0.):     # allgemein
    '''
    This Method is used for creation in Transformation Element build up from pointTypes for Translation, Scaling and Rotation
    Note that in CPACS 1.0 Translation should be of Type pointAbsRelType Due to TIGL issues this feature is still unabled inside the cpacslib.py
    @author: Jonas Jepsen
    @param parent: should be any Type holding a TransformationType
    @param tx, ty, tz, sx, sy, sz, rx, ry, rz:Translation, Scaling and Rotation   
    '''
    # Convert to CPACS Types

    myTranslation    = pointAbsRelType(refType=refType, x=doubleBaseType(valueOf_=str(tx)), y=doubleBaseType(valueOf_=str(ty)), z=doubleBaseType(valueOf_=str(tz)))
    myScaling        = pointType(x=doubleBaseType(valueOf_=str(sx)), y=doubleBaseType(valueOf_=str(sy)), z=doubleBaseType(valueOf_=str(sz)))
    myRotation       = pointType(x=doubleBaseType(valueOf_=str(rx)), y=doubleBaseType(valueOf_=str(ry)), z=doubleBaseType(valueOf_=str(rz)))
    
    #Create Element
    myTransformation = transformationType(scaling=myScaling, rotation=myRotation, translation=myTranslation )

    #Append to Parent
    parent.set_transformation(myTransformation)

def createPositioning(parent,uID,fromID,toID,length,sweep,dihedral,name):
    '''
    Create a positioning for Fuselage Elements
    parent Element should be of PositioningsType 
    from ID must not be given, if None then element is placed relative to origin
    uID will be saved as "positioning"+uID
    @author: Jonas Jepsen
    '''
    #Convert Types
    mytoID          = stringBaseType(None,None,None,toID)
    myName          = stringBaseType(None,None,None,name)
    myLength        = doubleBaseType(None,None,None,str(length))
    mySweep         = doubleBaseType(None,None,None,str(sweep))
    myDihedral      = doubleBaseType(None,None,None,str(dihedral))
    
    #Check if fromID is given
    #if it is given convert Type and create Positioning
    if fromID is not None:
        myfromID      = stringBaseType(None,None,None,fromID)
        myPositioning = positioningType(None,None,None,uID,myName,None,myLength,mySweep,myDihedral,myfromID,mytoID)
    #if no from ID is given create Positioning with None
    else:
        myPositioning = positioningType(None,None,None,uID,myName,None,myLength,mySweep,myDihedral,None,mytoID)
    
    #Add to parent
    parent.add_positioning(myPositioning)

def createPoint(parent,x,y,z=None):
    '''
    Methods builds a Point from PointType and adds it to parent
    @author: Jonas Jepsen
    @param parent: parent element (i.e. pointListType)
    @param x: X-Coordinate
    @param y: Y-Coordinate  
    @param z: Z-Coordinate, default is NONE
    '''
    xP = doubleBaseType(None, None, None,str(x))
    yP = doubleBaseType(None, None, None,str(0.0))
    zP = doubleBaseType(None, None, None,str(y))
    if z is None:
        myPoint = pointType(None, None, None, None, xP, yP ,None)
    else:
        zP = doubleBaseType(None, None, None,str(z))
        myPoint = pointType(None, None, None, None, xP, yP ,zP)
    parent.add_point(myPoint)


def calcLength(sweep, dihedral, dy):
    ''' 
    Method calculates lenght for the positioning from sweep, dihedral and the x-distance.
    @author: Jonas Jepsen
    @param sweep: sweep angle [in degrees]
    @param dihedral: dihedral angle [in degrees]
    @param dy: distance to the next section (along y-axis)
    @return: length
    '''
    
    length = dy/cos(dihedral/180.*pi)/cos(sweep/180.*pi)
    return length

def createPointList(pointList):
    #new Point List object 
    myPointList = pointListType(None, None, None, None)
    
    for [xvalue,yvalue] in pointList:
        #Convert Types and Create Point
        x = doubleBaseType(None, None, None,str(xvalue))
        y = doubleBaseType(None, None, None,str(yvalue))
        z = doubleBaseType(None, None, None,str(0.0))
        myPoint = pointType(None, None, None, None, x, y, z)
        #Add Point to PointList
        myPointList.add_point(myPoint)
    return myPointList

def createProfilefromList (myAirfoils,pointList,uID):
    '''
    Used for generation of Wing Profile from a simple 2D List
    @param myAirfoils: wingAirfoils object, Profile will be added here
    @param pointList: the pointlist of the profile
    @param uID: the uID for the profile
    @todo: allow overwriting existing airfoil with same uID
    @note: for now this function always creates a new airfoil
    '''
    #new Point List object 
    myPointList = createPointList(pointList)

    name            = stringBaseType(None, None, None,"Name"+uID)
    descripton      = stringBaseType(None, None, None,"Profile generated automatically by cpacs-export" )
    myAirfoils.add_wingAirfoil(profileGeometryType(None,None,None,uID, name, descripton, myPointList))
