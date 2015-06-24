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


from VAMPzero.Lib.CPACS.cpacs import stringBaseType, componentSegmentsType, \
    componentSegmentType, wingComponentSegmentStructureType, wingSparType, \
    sparPositionsType, sparSegmentsType, sparPositionType, doubleBaseType, \
    sparSegmentType, sparPositionUIDsType, sparCrossSectionType, stringUIDBaseType, \
    materialDefinitionType, capType, webType, wingSkinType, wingStringerType, \
    wingShellType, wingFuelTankBorderType, wingFuelTankGeometryType, \
    wingFuelTankType, wingFuelTanksType, wingRibCrossSectionType, ribRotationType, \
    wingRibsPositioningType, ribCrossingBehaviourType, wingRibsDefinitionType, \
    wingRibsDefinitionsType, integerBaseType, ribIdentificationType, \
    wingFuselageAttachmentType, wingFuselageAttachmentsType, wingWingAttachmentType, \
    wingWingAttachmentsType, wingWingAttachmentElementsType,wingWingAttachmentSparsType, \
    wingWingAttachmentsSparsType

from numpy.ma.core import ceil



def createComponentSegment(parent, parentUID, fromElement='_Sec1_Elem1'):
    '''
    Used for generation of componentSegments within a wing
    create numOfComponentSegs in a wing
    @param parent: wingType object, Sections-object will be added here
    @param parentUID:  UID of parent object [string]
    '''
    #===========================================================================
    # Create Component Segement
    #===========================================================================
    myUID = parentUID + '_Cseg'
    myName = stringBaseType(None, None, None, parentUID + '_CSeg')
    myDescr = stringBaseType(None, None, None, parentUID + '_CSeg')
    myFromElem = stringBaseType(None, None, None, parentUID + fromElement)
    index = str(len(parent.get_sections().get_section()))
    myToElem = stringBaseType(None, None, None, parentUID + '_Sec' + index + '_Elem1')
    myStructure = wingComponentSegmentStructureType()
    
    #===========================================================================
    # Back to CPACS
    #===========================================================================
    myComponentSegments = componentSegmentsType()
    myComponentSegment = componentSegmentType(None, None, None, myUID, myName, myDescr, myFromElem, myToElem, myStructure, None, None)
    myComponentSegments.add_componentSegment(myComponentSegment)
    parent.set_componentSegments(myComponentSegments)

def createSpars(parent, parentUID, typeOfSeg, etaFus=0.1, etaKink=0.3, cTip=1.0, cRoot=6.0):
    '''
    Used for generation of spars within a componentSegment
    @param parent: ComponentSegment object, spars-object will be added here

    @param etaFus:  eta Position at the Fuselage intersection
    @param etaKink: eta Position at the Kink
    @param typeOfSeg: either advDoubleTrapezoid or trapezoid or aileron
    
    .. todo:
    
       Maybe it would be a good idea to catch errors for high values of sweep
       and high kink ratios. For this case the spar maybe out of bounds of the inner wing! 
    '''
    mySparPositions = sparPositionsType(None, None, None, None)
    myUID = parentUID + '_Spar'
    
    #===========================================================================
    # Spar Postions
    #===========================================================================
    if typeOfSeg == 'advDoubletrapezoid':
        # The front spar should have a constant distance to the leading edge
        distance = cRoot * .1
        xsiRoot = distance / cRoot  
        xsiTip_front = distance / cTip
        xsiTip_rear = 0.59
        if xsiTip_front >= xsiTip_rear:
            xsiTip_rear = xsiTip_front + 0.1
        if xsiTip_rear > 1.0:
            print "VAMPzero Warning: Rear spar location at the tip is larger than 1. Increase Taper Ratio!!!"
        frontSparLocactions = [[0.0, xsiRoot], [etaFus, xsiRoot], [1.0, xsiTip_front]]
        rearSparLocactions = [[0.0, 0.56],  [etaFus, 0.56], [etaKink, 0.6], [1.0, xsiTip_rear]]

    if typeOfSeg == 'strutBracedWing':
        # The calculation of the strut braced wing is similar to that of the
        # double trapezoid wing. nevertheless, we exclude the kink spar position
        #
        # The front spar should have a constant distance to the leading edge
        distance = cRoot * .1
        xsiRoot = distance / cRoot
        xsiTip_front = distance / cTip
        xsiTip_rear = 0.59
        if xsiTip_front >= xsiTip_rear:
            xsiTip_rear = xsiTip_front + 0.1
        if xsiTip_rear > 1.0:
            print "VAMPzero Warning: Rear spar location at the tip is larger than 1. Increase Taper Ratio!!!"
        frontSparLocactions = [[0.0, xsiRoot], [etaFus, xsiRoot], [1.0, xsiTip_front]]
        rearSparLocactions = [[0.0, 0.56], [0.05, 0.56], [etaFus, 0.56], [1.0, xsiTip_rear]]

    if typeOfSeg == 'trapezoid':
        frontSparLocactions = [[0.0, 0.22], [1.0, 0.22]]
        rearSparLocactions = [[0.0, 0.55], [1.0, 0.55]]

    if typeOfSeg == 'strut':
        frontSparLocactions = [[0.0, 0.3], [1.0, 0.3]]
        rearSparLocactions = []

    if typeOfSeg == 'aileron':
        frontSparLocactions = [[0.0, 0.2], [1.0, 0.2]]
        rearSparLocactions = [[0.0, 0.7], [1.0, 0.7]]

    if typeOfSeg == 'flap' or typeOfSeg == 'innerFlap':
        frontSparLocactions = [[0.0, 0.2], [1.0, 0.2]]
        rearSparLocactions = [[0.0, 0.7], [1.0, 0.7]]

    if typeOfSeg == 'spoiler':
        frontSparLocactions = [[0.0, 0.2], [1.0, 0.2]]
        rearSparLocactions = []
        
    #===========================================================================
    # Assign Spar Locations 
    #===========================================================================
    for item in frontSparLocactions:
        x = doubleBaseType(valueOf_=str(item[0]))
        y = doubleBaseType(valueOf_=str(item[1]))
        mySparPostion = sparPositionType(None, None, None, myUID + '_FS_P' + str(frontSparLocactions.index(item)), eta=x, xsi=y)
        mySparPositions.add_sparPosition(mySparPostion)

    if len(rearSparLocactions) != 0:
        for item in rearSparLocactions:
            x = doubleBaseType(valueOf_=str(item[0]))
            y = doubleBaseType(valueOf_=str(item[1]))
            mySparPostion = sparPositionType(None, None, None, myUID + '_RS_P' + str(rearSparLocactions.index(item)), eta=x, xsi=y)
            mySparPositions.add_sparPosition(mySparPostion)
        
    #===========================================================================
    # Create Segments
    #===========================================================================
    mySparSegments = sparSegmentsType(None, None, None, None)
    createSparSegment(mySparSegments, myUID, '_FS', numOfPoints=len(frontSparLocactions), typeOfSeg=typeOfSeg)
    if len(rearSparLocactions) != 0:
        createSparSegment(mySparSegments, myUID, '_RS', numOfPoints=len(rearSparLocactions))
    
    #===========================================================================
    # Back to CPACS
    #===========================================================================
    mySpars = wingSparType(None, None, None, mySparPositions, mySparSegments)
    parent.get_structure().set_spars(mySpars)


def createSparSegment(parent, parentUID, targetUID='FS', material='aluminium7075', numOfPoints=3, typeOfSeg='other'):
    '''
    Used for generation of sparSegment within sparSegments
    @param parent: sparSegments, sparSegment will be added here

    @param id:  id of the spar either FS or RS
    @param material: uID of the material to be used
    @param numOfPoint: the number of SparPositions to position the spar
    '''
    myUID = parentUID + '' + targetUID
    myName = stringBaseType(None, None, None, myUID)
    myDescr = stringBaseType(None, None, None, myUID)
    
    #===========================================================================
    # Spar Position UIDS
    #===========================================================================
    mySparPositionUIDs = sparPositionUIDsType(None, None, None, None)
    for i in range(numOfPoints):
        sparPositionUID = stringUIDBaseType(None, None, None, None, myUID + '_P' + str(i))
        mySparPositionUIDs.add_sparPositionUID(sparPositionUID)
    
    #===========================================================================
    # Spar Cross Section
    #===========================================================================
    if typeOfSeg != 'strut':
        myMaterialUID = stringUIDBaseType(isLink='True', valueOf_=material)
        myThickness = doubleBaseType(valueOf_=str(0.003))
        myMaterial = materialDefinitionType(materialUID=myMaterialUID, thickness=myThickness)

    elif typeOfSeg =='strut':
        myMaterial = materialDefinitionType(compositeUID = stringUIDBaseType(isLink='True',valueOf_='Comp_Shear'), orthotropyDirection=doubleBaseType(valueOf_='0.'),\
                                         thicknessScaling=doubleBaseType(valueOf_='0.001'))

    myArea = doubleBaseType(None, None, None, str(0.0003))
    myCap = capType(None, None, None, myArea, myMaterial)
    
    myRelPos = doubleBaseType(None, None, None, str(0.5))
    myWeb = webType(None, None, None, myMaterial, myRelPos)
    
    myRotation = doubleBaseType(None, None, None, str(90.0))
    mySparCrossSection = sparCrossSectionType(None, None, None, myCap, myCap, myWeb, None, None, myRotation)
    
    #===========================================================================
    mySpar = sparSegmentType(None, None, None, myUID, myName, myDescr, mySparPositionUIDs, mySparCrossSection)
    parent.add_sparSegment(mySpar)

def createShell(parent, parentUID, typeOfSeg, thickness=0.003, pitch=0.14):
    '''
    Used for generation of wing upper and lower shell within a componentSegment
    @param parent: ComponentSegment object, upper and lower shell-object will be added here

    @param thickness:  thickness of the wing shell
    @param pitch: pitch of the stringers
    @param typeOfSeg: either advDoubleTrapezoid or trapezoid
    '''

    if typeOfSeg != 'strut':
        myAlu2024 = materialDefinitionType(materialUID=stringUIDBaseType(isLink='True', valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_=str(thickness)))
        myAlu7075 = materialDefinitionType(materialUID=stringUIDBaseType(isLink='True', valueOf_='aluminium7075'), thickness=doubleBaseType(valueOf_=str(thickness)))

        mySkin2024 = wingSkinType(material=myAlu2024)
        mySkin7075 = wingSkinType(material=myAlu7075)

        myStringerUp = wingStringerType(stringerStructureUID=stringUIDBaseType(valueOf_='Stringer_WING_up'), angle=doubleBaseType(valueOf_='0.0'), pitch=doubleBaseType(valueOf_=str(pitch)))
        myStringerLow = wingStringerType(stringerStructureUID=stringUIDBaseType(valueOf_='Stringer_WING_low'), angle=doubleBaseType(valueOf_='0.0'), pitch=doubleBaseType(valueOf_=str(pitch)))

        myShell2024 = wingShellType(uID='', skin=mySkin2024, stringer=myStringerLow)
        myShell7075 = wingShellType(uID='', skin=mySkin7075, stringer=myStringerUp)

        parent.get_structure().set_upperShell(myShell7075)
        parent.get_structure().set_lowerShell(myShell2024)

    elif typeOfSeg == 'strut':
        myComp_Long = materialDefinitionType(compositeUID = stringUIDBaseType(isLink='True',valueOf_='Comp_Long'), orthotropyDirection=doubleBaseType(valueOf_='0.'),\
                                         thicknessScaling=doubleBaseType(valueOf_='0.001'))

        mySkinComp = wingSkinType(material=myComp_Long)
        myShellComp = wingShellType(uID='', skin=mySkinComp)

        parent.get_structure().set_upperShell(myShellComp)
        parent.get_structure().set_lowerShell(myShellComp)


def createRibs(parent, parentUID, typeOfSeg, thickness=0.03, pitch=.8, nRibs=None, etaFus=0.2, etaEng=.3, span=17., fanDiameter=1.9, etaStrut=0.0, phi25 = 0.0):
    '''
    Used for generation of a ribs definition in the wing 

    @param parent: ComponentSegment object, ribsDefinition will be added here
    @param thickness:  thickness of the ribs
    @param pitch: pitch of the ribs
    @param typeOfSeg: either advDoubleTrapezoid or trapezoid
    '''
    myUID = parentUID + '_ribs'
    ribsList = []

    #===============================================================================
    # Advanced Double Trapezoid 
    #===============================================================================
    if typeOfSeg.lower() == 'advdoubletrapezoid':
        myName = stringBaseType(None, None, None, 'wing_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(None, None, None, None, None, None, stringUIDBaseType(None, None, 'True', None, 'aluminium7075'), \
                                              doubleBaseType(None, None, None, str(thickness)))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)
        ribReference = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribStart = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribEnd = stringBaseType(None, None, None, parentUID + '_Spar_RS')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'globalY'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')

        #=======================================================================
        # First set of 4 ribs inside the fuselage
        #=======================================================================
        etaStart = doubleBaseType(None, None, None, '0.0')
        etaEnd = doubleBaseType(None, None, None, str(etaFus))
        innerRibs = doubleBaseType(None, None, None, 4)
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, innerRibs, ribCrossing, ribRotation)
        
        myUID = parentUID + '_ribs_inner'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

        #===============================================================
        # Second set outside of the fuselage up to the engine
        #===============================================================
        etaPylon = 1. / 10. * fanDiameter / span
        etaStart = doubleBaseType(None, None, None, str(etaFus + pitch / span))
        etaEnd = doubleBaseType(None, None, None, str(etaEng - etaPylon))
        middleRibs = int(ceil((etaEng - etaPylon - etaFus) * span / pitch)) - 1
        if middleRibs < 1:
            middleRibs = 1
        middleRibs = doubleBaseType(None, None, None, middleRibs)
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, middleRibs, ribCrossing, ribRotation)
        
        myUID = parentUID + '_ribs_engine1'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

        #===============================================================
        # Third set one ribs outside of the pylon
        #===============================================================
        etaEnd = doubleBaseType(None, None, None, str(etaEng + etaPylon))
        pylonRibs = doubleBaseType(None, None, None, str(1))
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaEnd, etaEnd, ribStart, ribEnd, \
                                      None, pylonRibs, ribCrossing, ribRotation)
        
        myUID = parentUID + '_ribs_engine2'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

        
        #===============================================================
        # Fourth set outside of the engine
        #===============================================================
        etaStart = doubleBaseType(None, None, None, str(etaEng + etaPylon + pitch / span))
        etaEnd = doubleBaseType(None, None, None, '0.95')
        
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'end')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'wing_Spar_FS'), \
                                           doubleBaseType(None, None, None, '90.'))

        outerRibs = int(ceil((0.95 - etaEng + etaPylon) * span / pitch)) - 1
        outerRibs = doubleBaseType(None, None, None, outerRibs)

        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, outerRibs, ribCrossing, ribRotation)
        myUID = parentUID + '_ribs_outer'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

    #===============================================================================
    # Strut Braced Wing
    #===============================================================================
    if typeOfSeg.lower() == 'strutbracedwing':
        myName = stringBaseType(None, None, None, 'wing_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(None, None, None, None, None, None, stringUIDBaseType(None, None, 'True', None, 'aluminium7075'), \
                                              doubleBaseType(None, None, None, str(thickness)))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)
        ribReference = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribStart = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribEnd = stringBaseType(None, None, None, parentUID + '_Spar_RS')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'globalY'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')

        #=======================================================================
        # First set of 4 ribs inside the fuselage
        #=======================================================================
        etaStart = doubleBaseType(None, None, None, '0.0')
        etaEnd = doubleBaseType(None, None, None, str(etaFus))
        innerRibs = doubleBaseType(None, None, None, 4)
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, innerRibs, ribCrossing, ribRotation)

        myUID = parentUID + '_ribs_inner'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

        #===============================================================
        # Second set outside of the fuselage up to the strut
        #===============================================================
        etaStart = doubleBaseType(None, None, None, str(etaFus + pitch / span + phi25 * 0.0002))
        etaEnd = doubleBaseType(None, None, None, str(etaStrut))
        middleRibs = int(ceil((etaStrut - etaFus) * span / pitch)) - 1
        middleRibs = doubleBaseType(None, None, None, middleRibs)
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, middleRibs, ribCrossing, ribRotation)

        myUID = parentUID + '_ribs_strut'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

        #===============================================================
        # Third set outside of the spar
        #===============================================================
        etaStart = doubleBaseType(None, None, None, str(etaStrut + pitch / span))
        etaEnd = doubleBaseType(None, None, None, '0.95')

        ribCrossing = ribCrossingBehaviourType(None, None, None, 'end')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'wing_Spar_FS'), \
                                           doubleBaseType(None, None, None, '90.'))

        outerRibs = int(ceil((0.95 - etaStrut) * span / pitch)) - 1
        outerRibs = doubleBaseType(None, None, None, outerRibs)

        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, outerRibs, ribCrossing, ribRotation)
        myUID = parentUID + '_ribs_outer'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

    #===============================================================================
    # Strut (And only the strut not the wing that goes along with it)
    #===============================================================================
    if typeOfSeg.lower() == 'strut':
        myName = stringBaseType(None, None, None, 'strut_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(compositeUID=stringUIDBaseType(isLink='True',valueOf_='Comp_Shear'), orthotropyDirection=doubleBaseType(valueOf_='0.'),\
                                          thicknessScaling=doubleBaseType(valueOf_='0.001'))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)
        ribReference = stringBaseType(None, None, None, 'leadingEdge')
        ribStart = stringBaseType(None, None, None, 'leadingEdge')
        ribEnd = stringBaseType(None, None, None, 'trailingEdge')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'globalY'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')

        etaStart = doubleBaseType(None, None, None, str(0.001))
        etaEnd = doubleBaseType(None, None, None, str(0.999))
        #middleRibs = int(ceil(span / 0.70)) - 1
        middleRibs = doubleBaseType(None, None, None, 5.)
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, middleRibs, ribCrossing, ribRotation)

        myUID = parentUID + '_ribs'
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

    #===============================================================================
    # Aileron 
    #===============================================================================
    if typeOfSeg.lower() == 'aileron':
        myName = stringBaseType(None, None, None, 'aileron_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(None, None, None, None, None, None, stringUIDBaseType(None, None, 'True', None, 'aluminium2024'), \
                                              doubleBaseType(None, None, None, str(thickness)))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)
        
        # Rib Positioning
        #=======================================================================
        etaStart = doubleBaseType(None, None, None, '0.')
        etaEnd = doubleBaseType(None, None, None, '1.')
        ribReference = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribStart = stringBaseType(None, None, None, 'leadingEdge')
        ribEnd = stringBaseType(None, None, None, 'trailingEdge')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'globalY'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')
        if nRibs is None:
            ribSpacing = doubleBaseType(None, None, None, pitch)
            ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                          ribSpacing, None, ribCrossing, ribRotation)
        else: 
            nRibs = doubleBaseType(None, None, None, nRibs)
            ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                          None, nRibs, ribCrossing, ribRotation)
        
        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

    if typeOfSeg.lower() == 'trapezoid':
        myName = stringBaseType(None, None, None, 'trapezoid_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(None, None, None, None, None, None, stringUIDBaseType(None, None, 'True', None, 'aluminium2024'), \
                                              doubleBaseType(None, None, None, str(thickness)))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)

        # Rib Positioning
        #=======================================================================
        etaStart = doubleBaseType(None, None, None, '0.')
        etaEnd = doubleBaseType(None, None, None, '1.')
        ribReference = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribStart = stringBaseType(None, None, None, 'leadingEdge')
        ribEnd = stringBaseType(None, None, None, 'trailingEdge')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'globalY'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')

        etaStart = doubleBaseType(None, None, None, str(0.0))
        etaEnd = doubleBaseType(None, None, None, str(0.95))
        middleRibs = doubleBaseType(None, None, None, 5.)
        ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                      None, middleRibs, ribCrossing, ribRotation)

        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))

    #===============================================================================
    # Flap
    #===============================================================================
    if typeOfSeg.lower() == 'flap' or typeOfSeg.lower() == 'innerflap':
        myName = stringBaseType(None, None, None, 'flap_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(None, None, None, None, None, None, stringUIDBaseType(None, None, 'True', None, 'aluminium2024'), \
                                              doubleBaseType(None, None, None, str(thickness)))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)
        
        # Rib Positioning
        #=======================================================================
        etaStart = doubleBaseType(None, None, None, '0.')
        etaEnd = doubleBaseType(None, None, None, '1.')
        ribReference = stringBaseType(None, None, None, parentUID + '_Spar_FS')
        ribStart = stringBaseType(None, None, None, 'leadingEdge')
        ribEnd = stringBaseType(None, None, None, 'trailingEdge')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'globalY'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')
        if nRibs is None:
            ribSpacing = doubleBaseType(None, None, None, pitch)
            ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                          ribSpacing, None, ribCrossing, ribRotation)
        else: 
            nRibs = doubleBaseType(None, None, None, nRibs)
            ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                          None, nRibs, ribCrossing, ribRotation)

        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))
    #===============================================================================
    # Spoiler
    #===============================================================================
    if typeOfSeg.lower() == 'spoiler':
        myName = stringBaseType(None, None, None, 'spoiler_ribs')

        # Rib Cross Section
        #=======================================================================
        myMaterial = materialDefinitionType(None, None, None, None, None, None, stringUIDBaseType(None, None, 'True', None, 'aluminium2024'), \
                                              doubleBaseType(None, None, None, str(thickness)))
        myCrossSection = wingRibCrossSectionType(None, None, None, myMaterial, None)
        
        # Rib Positioning
        #=======================================================================
        etaStart = doubleBaseType(None, None, None, '0.')
        etaEnd = doubleBaseType(None, None, None, '1.')
        ribReference = stringBaseType(None, None, None, 'leadingEdge')
        ribStart = stringBaseType(None, None, None, 'leadingEdge')
        ribEnd = stringBaseType(None, None, None, 'trailingEdge')
        ribRotation = ribRotationType(None, None, None, stringBaseType(None, None, None, 'leadingEdge'), \
                                           doubleBaseType(None, None, None, '90.'))
        ribCrossing = ribCrossingBehaviourType(None, None, None, 'cross')
        if nRibs is None:
            ribSpacing = doubleBaseType(None, None, None, pitch)
            ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                          ribSpacing, None, ribCrossing, ribRotation)
        else: 
            nRibs = doubleBaseType(None, None, None, nRibs)
            ribsPositioning = wingRibsPositioningType(None, None, None, ribReference, etaStart, etaEnd, ribStart, ribEnd, \
                                          None, nRibs, ribCrossing, ribRotation)

        ribsList.append(wingRibsDefinitionType(None, None, None, myUID, myName, None, ribsPositioning, myCrossSection))
        
    #=======================================================================
    # RibsDefinition
    #=======================================================================
    
    myRibsDefinitions = wingRibsDefinitionsType(None, None, None, ribsList)
    
    parent.get_structure().set_ribsDefinitions(myRibsDefinitions)


def createTanks(parent, parentUID, targetUID='tank1', typeOfSeg='advDoubletrapezoid', nRib='2'):
    '''
    Used for generation of a wing tank

    @param parent: ComponentSegment object, wing fuel tank will be added here. 
    @param typeOfSeg: either advDoubleTrapezoid or trapezoid
    @param iRib: index of Rib in wing_ribs ribDefinition
    '''
    tanks = []

    #===========================================================================
    # Tanks
    #===========================================================================

    if typeOfSeg == 'advDoubletrapezoid':
        # Innermost
        myUID = parentUID + '_tank_inner'
        myName = stringBaseType(None, None, None, myUID)
        front = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_FS'))
        outer = wingFuelTankBorderType(ribDefinitionUID=stringUIDBaseType(valueOf_='wing_ribs_inner'), ribNumber=integerBaseType(valueOf_=str(4)))
        rear = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_RS'))
        myGeometry = wingFuelTankGeometryType(None, None, None, [front, outer, rear])
        tanks.append(wingFuelTankType(None, None, None, myUID, myName, None, myGeometry, None))

        # root to tw
        myUID = parentUID + '_tank_middle'
        myName = stringBaseType(None, None, None, myUID)
        inner = outer
        front = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_FS'))
        outer = wingFuelTankBorderType(ribDefinitionUID=stringUIDBaseType(valueOf_='wing_ribs_engine2'), ribNumber=integerBaseType(valueOf_=str(1)))
        rear = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_RS'))
        myGeometry = wingFuelTankGeometryType(None, None, None, [inner, front, outer, rear])
        tanks.append(wingFuelTankType(None, None, None, myUID, myName, None, myGeometry, None))

        # tw to outer
        myUID = parentUID + '_tank_outer'
        myName = stringBaseType(None, None, None, myUID)
        inner = outer
        front = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_FS'))
        outer = wingFuelTankBorderType(ribDefinitionUID=stringUIDBaseType(valueOf_=parentUID + '_ribs_outer'), ribNumber=integerBaseType(valueOf_=str(nRib)))
        rear = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_RS'))
        myGeometry = wingFuelTankGeometryType(None, None, None, [inner, front, outer, rear])
        tanks.append(wingFuelTankType(None, None, None, myUID, myName, None, myGeometry, None))

    if typeOfSeg == "strutBracedWing":
        # Innermost
        myUID = parentUID + '_tank_inner'
        myName = stringBaseType(None, None, None, myUID)
        front = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_FS'))
        outer = wingFuelTankBorderType(ribDefinitionUID=stringUIDBaseType(valueOf_='wing_ribs_inner'), ribNumber=integerBaseType(valueOf_=str(4)))
        rear = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_RS'))
        myGeometry = wingFuelTankGeometryType(None, None, None, [front, outer, rear])
        tanks.append(wingFuelTankType(None, None, None, myUID, myName, None, myGeometry, None))

        # root to strut
        myUID = parentUID + '_tank_middle'
        myName = stringBaseType(None, None, None, myUID)
        inner = outer
        front = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_FS'))
        outer = wingFuelTankBorderType(ribDefinitionUID=stringUIDBaseType(valueOf_='wing_ribs_outer'), ribNumber=integerBaseType(valueOf_=str(1)))
        rear = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_RS'))
        myGeometry = wingFuelTankGeometryType(None, None, None, [inner, front, outer, rear])
        tanks.append(wingFuelTankType(None, None, None, myUID, myName, None, myGeometry, None))

        # strut to outer
        myUID = parentUID + '_tank_outer'
        myName = stringBaseType(None, None, None, myUID)
        inner = outer
        front = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_FS'))
        outer = wingFuelTankBorderType(ribDefinitionUID=stringUIDBaseType(valueOf_=parentUID + '_ribs_outer'), ribNumber=integerBaseType(valueOf_=str(nRib)))
        rear = wingFuelTankBorderType(None, None, None, stringUIDBaseType(None, None, 'True', None, parentUID + '_Spar_RS'))
        myGeometry = wingFuelTankGeometryType(None, None, None, [inner, front, outer, rear])
        tanks.append(wingFuelTankType(None, None, None, myUID, myName, None, myGeometry, None))


    myTanks = wingFuelTanksType(None, None, None, tanks)
    parent.set_wingFuelTanks(myTanks)

def createWingFuselageAttachment(parent, parentUID, targetUID='fuselage', typeOfSeg='advDoubletrapezoid'):

    if typeOfSeg == 'advDoubletrapezoid':
        toFuselageUID = stringUIDBaseType(valueOf_=targetUID)
        rib1 = ribIdentificationType(ribDefinitionUID=stringUIDBaseType(valueOf_='wing_ribs_inner'), ribNumber=integerBaseType(valueOf_=str(4)))
        wingFuselageAttachment = wingFuselageAttachmentType(rib1=rib1)

    if typeOfSeg =='strut':
        toFuselageUID = stringUIDBaseType(valueOf_=targetUID)
        rib1 = ribIdentificationType(ribDefinitionUID=stringUIDBaseType(valueOf_='strut_ribs'), ribNumber=integerBaseType(valueOf_=str(1)))
        wingFuselageAttachment = wingFuselageAttachmentType(rib1=rib1)

    wingFuselageAttachments = wingFuselageAttachmentsType(wingFuselageAttachment=[wingFuselageAttachment])
    parent.set_wingFuselageAttachments(wingFuselageAttachments)

def createWingWingAttachment(parent, parentUID, targetUID='wing_Cseg', typeOfSeg='strut'):
    if typeOfSeg =='strut':
        toComponentSegmentUID = stringUIDBaseType(valueOf_=targetUID)

        fromElementUID = stringUIDBaseType(valueOf_='strut_Sec3_Elem1')
        toElementUID = stringUIDBaseType(valueOf_='wing_Sec3_Elem1')
        elements = wingWingAttachmentElementsType(fromElementUID=fromElementUID, toElementUID=toElementUID)

        fromSparUID = stringUIDBaseType(valueOf_='strut_Spar_FS')
        toSparUID = stringUIDBaseType(valueOf_='wing_Spar_FS')
        sparAttachment = wingWingAttachmentSparsType(fromSparUID=fromSparUID, toSparUID=toSparUID)
        sparAttachments = wingWingAttachmentsSparsType(sparAttachment=[sparAttachment])

        upperShellAttachment= stringUIDBaseType(valueOf_='upperShell')
        lowerShellAttachment= stringUIDBaseType(valueOf_='lowerShell')

        wingWingAttachment = wingWingAttachmentType(toComponentSegmentUID=toComponentSegmentUID, elements=elements, sparAttachments=sparAttachments, upperShellAttachment=upperShellAttachment, lowerShellAttachment=lowerShellAttachment)

    elif typeOfSeg == 'ttail':
        toComponentSegmentUID = stringUIDBaseType(valueOf_=targetUID)

        fromElementUID = stringUIDBaseType(valueOf_='htp_Sec1_Elem1')
        toElementUID = stringUIDBaseType(valueOf_='vtp_Sec2_Elem1')
        elements = wingWingAttachmentElementsType(fromElementUID=fromElementUID, toElementUID=toElementUID)

        fromSparUID = stringUIDBaseType(valueOf_='htp_Spar_FS')
        toSparUID = stringUIDBaseType(valueOf_='vtp_Spar_FS')
        FS_sparAttachment = wingWingAttachmentSparsType(fromSparUID=fromSparUID, toSparUID=toSparUID)

        fromSparUID = stringUIDBaseType(valueOf_='htp_Spar_RS')
        toSparUID = stringUIDBaseType(valueOf_='vtp_Spar_RS')
        RS_sparAttachment = wingWingAttachmentSparsType(fromSparUID=fromSparUID, toSparUID=toSparUID)

        sparAttachments = wingWingAttachmentsSparsType(sparAttachment=[FS_sparAttachment, RS_sparAttachment])

        upperShellAttachment= stringUIDBaseType(valueOf_='upperShell')
        lowerShellAttachment= stringUIDBaseType(valueOf_='lowerShell')

        wingWingAttachment = wingWingAttachmentType(toComponentSegmentUID=toComponentSegmentUID, elements=elements, sparAttachments=sparAttachments, upperShellAttachment=upperShellAttachment, lowerShellAttachment=lowerShellAttachment)


    wingWingAttachments = wingWingAttachmentsType(wingWingAttachment=[wingWingAttachment])
    parent.set_wingWingAttachments(wingWingAttachments)
