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

from VAMPzero.Lib.CPACS.Export.Wing.Shape.profiles import NACA0009, NACA653218
from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath, createTransformation
from VAMPzero.Lib.CPACS.cpacs import stringBaseType, wingSectionsType, \
    wingSegmentsType, wingSegmentType, wingSectionType, wingElementsType, \
    wingElementType, stringVectorBaseType, \
    pointListXYZVectorType



def createWingAirfoil(CPACSObj):
    # get airfoil holding object
    cpacsPath = '/cpacs/vehicles/profiles/wingAirfoils/wingAirfoil[NACA0009]'
    myAirfoil = getObjfromXpath(CPACSObj, cpacsPath)
    pointList = myAirfoil.get_pointList()
    if pointList is None:
        # print "Airfoil 'NACA0009' not found -> will be created."
        # create pointList
        pointList = pointListXYZVectorType()
        xVector = [] 
        yVector = []
        zVector = []
        
        
        
        for x, y in NACA0009:
            xVector.append(str(x))
            yVector.append(str(0.0))
            zVector.append(str(y))
        

        
        x = stringVectorBaseType(None, None, None, 'vector', ';'.join(xVector))
        y = stringVectorBaseType(None, None, None, 'vector', ';'.join(yVector))
        z = stringVectorBaseType(None, None, None, 'vector', ';'.join(zVector))
        
        pointList.set_x(x)
        pointList.set_y(y)
        pointList.set_z(z)
    
        myAirfoil.set_pointList(pointList)
        myAirfoil.set_name(stringBaseType(None, None, None, "NACA0009 Airfoil"))
        myAirfoil.set_description(stringBaseType(None, None, None, "Profile generated automatically by VAMPzero cpacs-export"))

    
    
    
    # get airfoil holding object
    cpacsPath = '/cpacs/vehicles/profiles/wingAirfoils/wingAirfoil[NACA653218]'
    myAirfoil = getObjfromXpath(CPACSObj, cpacsPath)
    pointList = myAirfoil.get_pointList()

    if pointList is None:
        # print "Airfoil 'NACA0000' not found -> will be created."
        # create pointList
        pointList = pointListXYZVectorType()
        xVector = [] 
        yVector = []
        zVector = []
        
        
        
        for x, y in NACA653218:
            xVector.append(str(x))
            yVector.append(str(0.0))
            zVector.append(str(y))
        

        
        x = stringVectorBaseType(None, None, None, 'vector', ';'.join(xVector))
        y = stringVectorBaseType(None, None, None, 'vector', ';'.join(yVector))
        z = stringVectorBaseType(None, None, None, 'vector', ';'.join(zVector))
        
        pointList.set_x(x)
        pointList.set_y(y)
        pointList.set_z(z)
        
        myAirfoil.set_pointList(pointList)
        myAirfoil.set_name(stringBaseType(None, None, None, "NACA653218 Airfoil"))
        myAirfoil.set_description(stringBaseType(None, None, None, "Profile generated automatically by VAMPzero cpacs-export"))

def createWingSection(parent, thickness, tx, ty, tz, sx, sy, sz, rx, ry, rz, AirfUID, maxT, UID='WSec', Name='WSec', descr='Wing Section'):
    '''
    Used for generation of a wing Section.
    Creates all the sections given through myQSi.
    @param parent: wingSectionsType object, wingSectionType-objects will be added here
    @param crossSection: only one cross section from PrADOs R1GEO**i (with ** as F,HL,SL,WL and i as wingindex)
    @param AirfUID: the AirfoilUID for this section
    @param maxT: the max profile thickness of this section
    @param UID:  UID of this section [string]
    @param Name: Name of this section [string]
    @param descr: Description of this section [string]
    '''
    # # ONLY ONE ELEMENT PER SECTION SUPPORTED
    mySection = wingSectionType(uID=UID)
    mySection.set_name(stringBaseType(None, None, None, Name))
    mySection.set_description(stringBaseType(None, None, None, descr))
    
    # Position of the Element
    createTransformation(mySection, 'absGlobal', tx, ty, tz, sx, sy, sz, rx, ry, rz,)
    myElements = wingElementsType()
    def createWingElement(parent, tx, ty, tz, sx, sy, sz, rx, ry, rz, AirfUID, UID='WElem', Name='WElem', descr='Wing Element'):
        '''
        Used for the creation of a wing element from PrADO cross section
        @param parent: wingElementsType object, element will be added here
        @param crossSection: the cross section parameters from PrADO [list] (see myFQS in PrADOlib/Wings.py)
        @param AirfUID: the uID of the used Profile
        @param UID: the UID of this element
        @param Name: Name of this Element [string]
        @param descr: Description of this Element [string]
        '''
        myElement = wingElementType(uID=UID)
        myElement.set_name(stringBaseType(None, None, None, Name))
        myElement.set_description(stringBaseType(None, None, None, descr))
        myElement.set_airfoilUID(stringBaseType(None, None, None, AirfUID))
        # Translation
        createTransformation(myElement, 'absGlobal', tx, ty, tz, sx, sy, sz, rx, ry, rz)
        parent.add_element(myElement)
    
    createWingElement(myElements, 0., 0., 0., 1., 1., thickness, 0., 0., 0., AirfUID, UID + '_Elem' + str(1), Name + '_Elem' + str(1), descr + '_Element' + str(1))
    mySection.set_elements(myElements)
    parent.add_section(mySection)

def createWingSections(parent, myQSi, ProfUIDs, maxTs, strUID, strName, strDescr):
    '''
    Used for generation of wing Sections.
    Creates all the sections given through myQSi.
    @param parent: wingType object, Sections-object will be added here
    @param myQSi: cross Sections from PrADOs R1GEO**i (with ** as F,HL,SL,WL and i as wingindex)
    @param ProfUIDs: list of ProfileUIDs in the same order as cross sections in myQSi
    @param maxTs: list of max profile thickness in the same order as cross sections in myQSi
    @param strUID:  UID of Sections [string]
    @param strName: Name of Sections [string]
    @param strDescr: Description of Sections [string]
    '''
    mySections = wingSectionsType()
    # countAll counts the total amount of cross sections for this fuselage
    countAll = 0
    for cs in myQSi:
        countAll += 1
        # create Section
        createWingSection(mySections, cs, ProfUIDs[countAll - 1], maxTs[countAll - 1], strUID + '_Sec' + str(countAll), strName + '_Sec' + str(countAll), strDescr + '_Sec' + str(countAll))
    parent.set_sections(mySections)

def createWingSegments(parent, parentUID, numOfSeg):
    '''
    Used for generation of wing Segments.
    Connects two sections to one segment.
    This method assumes, that two sections with contiguous numbers must be connected.
    @param parent: wingType object, Sections-object will be added here
    @param parentUID:  UID of parent object [string]
    @param numOfSeg: number of Segments to create (must be one less than sections)
    '''
    # # ONLY ONE ELEMENT PER SECTION SUPPORTED
    mySegments = wingSegmentsType()
    for i in range(numOfSeg):
        myUID = parentUID + '_Seg' + str(i + 1)
        myName = stringBaseType(None, None, None, parentUID + '_Seg' + str(i + 1))
        myDescr = stringBaseType(None, None, None, parentUID + '_Seg' + str(i + 1))
        myFromElem = stringBaseType(None, None, None, parentUID + '_Sec' + str(i + 1) + '_Elem1')
        myToElem = stringBaseType(None, None, None, parentUID + '_Sec' + str(i + 2) + '_Elem1')
        tmpSegment = wingSegmentType(None, None, None, myUID, myName, myDescr, myFromElem, myToElem)
        mySegments.add_segment(tmpSegment)
    parent.set_segments(mySegments)

