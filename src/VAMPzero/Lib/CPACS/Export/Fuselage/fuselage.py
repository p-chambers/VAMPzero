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

from math import pi

from VAMPzero.Lib.CPACS.cpacs import stringBaseType,\
    fuselageSectionType, fuselageSectionsType, fuselageElementType,\
    fuselageSegmentType, fuselageSegmentsType, positioningsType,\
    fuselageElementsType, pointListXYZVectorType, stringVectorBaseType
from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath, \
    createTransformation, createPositioning
from VAMPzero.Lib.CPACS.Export.Fuselage.profiles import createCircleList, NOSE, CABIN, TAIL
from VAMPzero.Lib.CPACS.Export.enums import FUSE_LOD

rad = pi / 180.

def createFuselage(CPACSObj, id, dfus, lnose, lcabin, ltail, LoD=0):
    # just for now
    if LoD==FUSE_LOD.NONE:
        return

    cpacsPath = '/cpacs/vehicles/aircraft/model/fuselages/fuselage[' + id + ']'
    # the next line is the one to use later on
    #cpacsPath = '/cpacs/vehicles/aircraft/model[model]/fuselages/fuselage[' + self.id + ']'
    # gets a list of all wing elements
    myFuse = getObjfromXpath(CPACSObj,cpacsPath)
    
    strUID       = myFuse.get_uID()
    myUID        = strUID
    myName       = stringBaseType(None,None,None,id)
    myDescr      = stringBaseType(None,None,None,strUID)
    myFuse.set_uID(myUID)
    myFuse.set_name(myName)
    myFuse.set_description(myDescr)
    
    createTransformation(myFuse, 'absGlobal',0.,0.,0.)
    
    if LoD==FUSE_LOD.A320:
        nose = list(NOSE)
        cabin = list(CABIN)
        tail = list(TAIL)
        # remove double values
        cabin.pop(0)
        tail.pop(0)
        # sections will be created, all existing sections will be deleted
        createFuselageSections(myFuse, nose,cabin,tail, dfus, strUID, strUID, strUID)
        createFuselagePositionings(myFuse, nose,cabin,tail, lnose,lcabin,ltail, strUID, strUID)
        
        createFuselageSegments(myFuse, strUID, len(nose)+len(cabin)+len(tail)-1)
    
    elif LoD==FUSE_LOD.ZYL:
        # sections will be created, all existing sections will be deleted
        mySections = fuselageSectionsType()
        #calc fuselage radius
        #rfus = dfus/2.
        # make fuselage configuration data [x_rel,z-dist,height/2,width/2]]
        fuseConf = [0.,0.,0.5,0.5]
        createFuselageSection(mySections, dfus, fuseConf, 'Circle', strUID+'_Sec1', strUID+'_Sec1', strUID+'_Sec1')
        createFuselageSection(mySections, dfus, fuseConf, 'Circle', strUID+'_Sec2', strUID+'_Sec2', strUID+'_Sec2')
        createFuselageSection(mySections, dfus, fuseConf, 'Circle', strUID+'_Sec3', strUID+'_Sec3', strUID+'_Sec3')
        createFuselageSection(mySections, dfus, fuseConf, 'Circle', strUID+'_Sec4', strUID+'_Sec4', strUID+'_Sec4')
        myFuse.set_sections(mySections)
                
        myPositionings = positioningsType()
        createPositioning(myPositionings,str(id) + '_Pos1',None, str(id) + '_Sec1',0.,90.,0.,id + '_Pos1')
        createPositioning(myPositionings,str(id) + '_Pos2',str(id) + '_Sec1',str(id) + '_Sec2',lnose,90.,0,id + '_Pos2')
        createPositioning(myPositionings,str(id) + '_Pos3',str(id) + '_Sec2',str(id) + '_Sec3',lcabin,90.,0,id + '_Pos3')
        createPositioning(myPositionings,str(id) + '_Pos4',str(id) + '_Sec3',str(id) + '_Sec4',ltail,90.,0,id + '_Pos4')
        myFuse.set_positionings(myPositionings)
        
        createFuselageSegments(myFuse, strUID, 3)
    
    
    

def createFuselagePositionings(parent, nose,cabin,tail, lnose,lcabin,ltail, strUID, strName):
    '''
    This method is used to create the positioning of the sections of a fuselage.
    It calculates the sweep and length.
    @author: Jonas Jepsen
    @param parent: could be any Type holding a positioningsType. Here [fuselageType]
    @param myRQSi: crosssection data
    @param strUID:  UID of this Positioning [string]
    @param strName: Name of this Positioning [string]
    '''
    myPositionings = positioningsType()
    # countAll counts the total amount of cross sections for this fuselage
    countAll = 0
    for part in [[nose,lnose],[cabin,lcabin],[tail,ltail]]: 
        # lastPos is used to calc the lenght of a Segment from the absolute position
        # reset lastPos to 0 after each part because positions are given in relative koordinates from 0 to 1 in each part (nose,cabine and tail)
        lastPos = 0.
        # create positionings
        for cs in part[0]:
            countAll += 1
            pos = cs[0]*part[1]
            # create Positionings
            if countAll <= 1:
                createPositioning(myPositionings, strUID+'_Pos'+str(countAll),None,strUID+'_Sec'+str(countAll),pos,90.,0.,strName+'_Position'+str(countAll))
            else:
                createPositioning(myPositionings, strUID+'_Pos'+str(countAll),strUID+'_Sec'+str(countAll-1),strUID+'_Sec'+str(countAll),pos-lastPos,90.,0.,strName+'_Position'+str(countAll))
            lastPos = pos
    
    parent.set_positionings(myPositionings)


def createFuselageProfile(CPACSObj, profile='Circle' ):
    '''
    @author: Jonas Jepsen
    '''
    # get airfoil holding object
    cpacsPath = '/cpacs/vehicles/profiles/fuselageProfiles/fuselageProfile[%s]'% profile
    myProfile = getObjfromXpath(CPACSObj,cpacsPath)
    pointList = myProfile.get_pointList()
    if pointList is None:
        #print "Airfoil 'Circle' not found -> will be created."
        xVector, yVector, zVector = createCircleList()
        # create pointList
        pointList   = pointListXYZVectorType()

        x         = stringVectorBaseType(None,None,None,'vector',';'.join(xVector))
        y         = stringVectorBaseType(None,None,None,'vector',';'.join(yVector))
        z         = stringVectorBaseType(None,None,None,'vector',';'.join(zVector))
        
        pointList.set_x(x)
        pointList.set_y(y)
        pointList.set_z(z)
        
        myProfile.set_pointList(pointList)
        myProfile.set_name(stringBaseType(None, None, None,"Circle Profile"))
        myProfile.set_description(stringBaseType(None, None, None,"Profile generated automatically by VAMPzero cpacs-export" ))


def createFuselageSection(parent, dfus, cs, ProfUID, UID='FLSec', Name='FLSec', descr='Fuselage Section'):
    '''
    Used for generation of a fuselage Section.
    Creates all the sections given through myRQSi.
    @author: Jonas Jepsen
    @param parent: fuselageSectionsType object, fuselageSectionType-objects will be added here
    @param crossSection: only one cross section from PrADO [x_rel,z-dist,height/2,width/2]
    @param ProfUID: the ProfileUID for this section
    @param UID:  UID of this section [string]
    @param Name: Name of this section [string]
    @param descr: Description of this section [string]
    '''
    ## ONLY ONE ELEMENT PER SECTION SUPPORTED
    mySection = fuselageSectionType(uID=UID)
    mySection.set_name(stringBaseType(None,None,None,Name))
    mySection.set_description(stringBaseType(None,None,None,descr))
    
    transZ = cs[1]*dfus
    scaleX = cs[3]*dfus
    scaleZ = cs[2]*dfus
    createTransformation(mySection,'absGlobal',0.,0.,transZ, 1.,1.,1., 0.,0.,0.)
    myElements = fuselageElementsType()
    def createFuselageElement(parent, sx,sz, profUID, UID='FLElem', Name='FLElem', descr='Fuselage Element'):
        '''
        Used for the creation of a fuselage element from PrADO cross section
        @author: Jonas Jepsen
        @param parent: fuselageElementsType object, element will be added here
        @param crossSection: the cross section parameters from PrADO [list] (see myRQS in PrADOlib/Fuselages.py)
        @param profUID: the uID of the used Profile
        @param UID: the UID of this element
        @param Name: Name of this Element [string]
        @param descr: Description of this Element [string]
        '''
        myElement = fuselageElementType(uID = UID)
        myElement.set_name(stringBaseType(None,None,None,Name))
        myElement.set_description(stringBaseType(None,None,None,descr))
        myElement.set_profileUID(stringBaseType(None,None,None,profUID))
        createTransformation(myElement,'absGlobal', 0.,0.,0., 1.,sx,sz, 0.,0.,0.)
        parent.add_element(myElement)
    
    createFuselageElement(myElements, scaleX,scaleZ, ProfUID, UID+'_Elem'+str(1), Name+'_Elem'+str(1), descr+'_Element'+str(1))
    mySection.set_elements(myElements)
    parent.add_section(mySection)

def createFuselageSections(parent, nose,cabin,tail, dfus, strUID, strName, strDescr):
    '''
    Used for generation of fuselage Sections.
    Creates all the sections given through myRQSi.
    @author: Jonas Jepsen
    @param parent: fuselageType object, Sections-object will be added here
    @param confList: cross Sections from PrADO for section configurations
    @param strUID:  UID of Sections [string]
    @param strName: Name of Sections [string]
    @param strDescr: Description of Sections [string]
    '''
    mySections = fuselageSectionsType()
    # countAll counts the total amount of cross sections for this fuselage
    countAll = 0
    for cs in nose:
        countAll += 1
        # create Section
        createFuselageSection(mySections, dfus, cs, 'Circle', strUID+'_Sec'+str(countAll), strName+'_Sec'+str(countAll), strDescr+'_Sec'+str(countAll))
    for cs in cabin:
        countAll += 1
        # create Section
        createFuselageSection(mySections, dfus, cs, 'Circle', strUID+'_Sec'+str(countAll), strName+'_Sec'+str(countAll), strDescr+'_Sec'+str(countAll))
    for cs in tail:
        countAll += 1
        # create Section
        createFuselageSection(mySections, dfus, cs, 'Circle', strUID+'_Sec'+str(countAll), strName+'_Sec'+str(countAll), strDescr+'_Sec'+str(countAll))
        
    parent.set_sections(mySections)

def createFuselageSegments(parent, parentUID, numOfSeg):
    '''
    Used for generation of fuselage Segments.
    Connects two sections to one segment.
    This method assumes, that two sections with contiguous numbers must be connected.
    @author: Jonas Jepsen
    @param parent: fuselageType object, Sections-object will be added here
    @param parentUID:  UID of parent object [string]
    @param numOfSeg: number of Segments to create (must be one less than sections)
    '''
    mySegments = fuselageSegmentsType()
    for i in range(numOfSeg):
        myUID       = parentUID+'_Seg'+str(i+1)
        myName      = stringBaseType(None,None,None,parentUID+'_Seg'+str(i+1))
        myDescr     = stringBaseType(None,None,None,parentUID+'_Seg'+str(i+1))
        myFromElem  = stringBaseType(None,None,None,parentUID+'_Sec'+str(i+1)+'_Elem1')
        myToElem    = stringBaseType(None,None,None,parentUID+'_Sec'+str(i+2)+'_Elem1')
        tmpSegment = fuselageSegmentType(None,None,None, myUID, myName, myDescr, myFromElem, myToElem)
        mySegments.add_segment(tmpSegment)
    parent.set_segments(mySegments)
