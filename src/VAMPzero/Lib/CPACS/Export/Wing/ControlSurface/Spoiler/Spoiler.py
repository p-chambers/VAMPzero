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
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Flap.Flap import \
    calcChordLengthAtEta
from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath
from VAMPzero.Lib.CPACS.cpacs import controlSurfaceBorderSpoilerType, \
    leadingEdgeShapeType, doubleBaseType, controlSurfacesType, \
    controlSurfaceOuterShapeSpoilerType, stringBaseType, leadingEdgeDevicesType, \
    leadingEdgeDeviceType, stringUIDBaseType, spoilersType, \
    wingComponentSegmentStructureType, spoilerType
from math import pi, ceil, tan, atan, sin, cos
from types import NoneType
import scipy.interpolate
from VAMPzero.Lib.Log.log import zeroLogger
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createShell, \
    createSpars, createRibs


rad = pi / 180.
log = zeroLogger('Spoiler')

def createSpoilers(parentWingCPACS, parentWingVAMPzero, mySpoiler):
    '''
    This is the main export method for the wing's spoilers
    
    * It assumes a constant absolut chord for all spoilers
    * Spoiler start outboard and move inboard close behind the rearspar
    * They are rectangular
    
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentWingVAMPzero.id + ']'
    cpacsWing = getObjfromXpath(parentWingCPACS, cpacsPath)
    cpacsComponentSegment = cpacsWing.get_componentSegments().get_componentSegment()[0]
    mySpoilers = []

    #===========================================================================
    # Initialization, i.e. fetching values throughout the code
    #===========================================================================
    span = parentWingVAMPzero.span.getValue() / 2.
    etaKink = parentWingVAMPzero.etaKink.getValue()
    yFus = parentWingVAMPzero.yFuselage.getValue()
    etaFus = yFus / span
 
    spoilerArea = mySpoiler.refArea.getValue()
    spoilerChord = mySpoiler.chord.getValue()
    spoilerOuterEta = mySpoiler.outerEta.getValue()
    
    sparOffset = 0.02

    #===========================================================================
    # Rear spar locations
    #===========================================================================
    xsiSparRoot = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[3].get_xsi().valueOf_)
    xsiSparFuselage = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[4].get_xsi().valueOf_)
    xsiSparKink = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[5].get_xsi().valueOf_)
    xsiSparTip = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[6].get_xsi().valueOf_)

    etaSparRoot = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[3].get_eta().valueOf_)
    etaSparFuselage = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[4].get_eta().valueOf_)
    etaSparKink = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[5].get_eta().valueOf_)
    etaSparTip = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[6].get_eta().valueOf_)

    xsiSpar_interp = scipy.interpolate.interp1d([etaSparRoot, etaSparFuselage, etaSparKink, etaSparTip], [xsiSparRoot, xsiSparFuselage, xsiSparKink, xsiSparTip])

    
    #===========================================================================
    # Outer Spoilers 
    #===========================================================================
    outerSpan = (spoilerOuterEta - etaKink) * span
    outerArea = spoilerChord * outerSpan
    nOuterSpoiler = outerSpan ** 2 / (outerArea * 2.)
    log.debug('VAMPzero SPOILER: Exporting %s Spoiler outside of the kink for an area of %s m2.' % (str(nOuterSpoiler), str(outerArea)))


    #===========================================================================
    # 1 Spoiler
    #===========================================================================
    if nOuterSpoiler <= 1.:
        # The outer eta of the leading Edge is correspondent to the outerEta of the spoiler 
        outerEtaLE = spoilerOuterEta
        # The inner eta of the leading edge is the outer eta minus the span of the outer spoiler 
        innerEtaLE = spoilerOuterEta - outerSpan / span
        # The inner and outer Xsi coordinate of the leading edge are defined by the rear spar location and the sparOffset
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset
        
        spoilerPhi = calcPhiLESpoiler(outerEtaLE, innerEtaLE, outerXsiLE, innerXsiLE, parentWingVAMPzero, cpacsWing)
        deltaEta = sin(spoilerPhi) * spoilerChord
        deltaXsi = cos(spoilerPhi) * spoilerChord
        
        outerEtaTE = outerEtaLE - deltaEta / span
        outerXsiTE = outerXsiLE + deltaXsi / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE - deltaEta / span
        innerXsiTE = innerXsiLE + deltaXsi / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        # We do not want the spoiler to overlap the kink as the inner Spoilers will start here
        if innerEtaTE < etaKink:
            innerEtaTE = etaKink
            innerXsiTE = innerXsiLE + spoilerChord / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        
        mySpoilers.append(createSpoiler('OuterSpoiler1', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))

    #===========================================================================
    # 2 Spoiler
    #===========================================================================
    elif nOuterSpoiler > 1. and nOuterSpoiler <= 2.:
        # The outer eta of the leading Edge is correspondent to the outerEta of the spoiler 
        outerEtaLE = spoilerOuterEta
        # The inner eta of the leading edge is the outer eta minus the span of the outer spoiler 
        innerEtaLE = spoilerOuterEta - outerSpan / span / 2.
        # The inner and outer Xsi coordinate of the leading edge are defined by the rear spar location and the sparOffset
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset
        
        spoilerPhi = calcPhiLESpoiler(outerEtaLE, innerEtaLE, outerXsiLE, innerXsiLE, parentWingVAMPzero, cpacsWing)
        deltaEta = sin(spoilerPhi) * spoilerChord
        deltaXsi = cos(spoilerPhi) * spoilerChord
        
        outerEtaTE = outerEtaLE - deltaEta / span
        outerXsiTE = outerXsiLE + deltaXsi / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE - deltaEta / span
        innerXsiTE = innerXsiLE + deltaXsi / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        
        mySpoilers.append(createSpoiler('OuterSpoiler2', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))

        # old outer is new inner 
        outerEtaLE = innerEtaLE
        # new inner is min next to kink  
        innerEtaLE = spoilerOuterEta - outerSpan / span
        # The inner and outer Xsi coordinate of the leading edge are defined by the rear spar location and the sparOffset
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset
        
        spoilerPhi = calcPhiLESpoiler(outerEtaLE, innerEtaLE, outerXsiLE, innerXsiLE, parentWingVAMPzero, cpacsWing)
        deltaEta = sin(spoilerPhi) * spoilerChord
        deltaXsi = cos(spoilerPhi) * spoilerChord
        
        outerEtaTE = outerEtaLE - deltaEta / span
        outerXsiTE = outerXsiLE + deltaXsi / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE - deltaEta / span
        innerXsiTE = innerXsiLE + deltaXsi / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        # We do not want the spoiler to overlap the kink as the inner Spoilers will start here
        if innerEtaTE < etaKink:
            innerEtaTE = etaKink
            innerXsiTE = innerXsiLE + spoilerChord / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        mySpoilers.append(createSpoiler('OuterSpoiler1', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))

    #===========================================================================
    # n Spoiler
    #===========================================================================
    elif nOuterSpoiler > 2.:
        n = int(ceil(nOuterSpoiler))
        # The outer eta of the leading Edge is correspondent to the outerEta of the spoiler 
        outerEtaLE = spoilerOuterEta
        # The inner eta of the leading edge is the outer eta minus the span of the outer spoiler 
        innerEtaLE = outerEtaLE - outerSpan / span / n
        # The inner and outer Xsi coordinate of the leading edge are defined by the rear spar location and the sparOffset
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset
        
        spoilerPhi = calcPhiLESpoiler(outerEtaLE, innerEtaLE, outerXsiLE, innerXsiLE, parentWingVAMPzero, cpacsWing)
        deltaEta = sin(spoilerPhi) * spoilerChord
        deltaXsi = cos(spoilerPhi) * spoilerChord
        
        outerEtaTE = outerEtaLE - deltaEta / span
        outerXsiTE = outerXsiLE + deltaXsi / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE - deltaEta / span
        innerXsiTE = innerXsiLE + deltaXsi / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        mySpoilers.append(createSpoiler('OuterSpoiler' + str(n), parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))

        for i in range(2, n):
            # old outer is new inner 
            outerEtaLE = innerEtaLE
            # new inner is min next to kink  
            innerEtaLE = outerEtaLE - outerSpan / span / n
            # The inner and outer Xsi coordinate of the leading edge are defined by the rear spar location and the sparOffset
            outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
            innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset
            
            spoilerPhi = calcPhiLESpoiler(outerEtaLE, innerEtaLE, outerXsiLE, innerXsiLE, parentWingVAMPzero, cpacsWing)
            deltaEta = sin(spoilerPhi) * spoilerChord
            deltaXsi = cos(spoilerPhi) * spoilerChord
            
            outerEtaTE = outerEtaLE - deltaEta / span
            outerXsiTE = outerXsiLE + deltaXsi / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
            innerEtaTE = innerEtaLE - deltaEta / span
            innerXsiTE = innerXsiLE + deltaXsi / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
            mySpoilers.append(createSpoiler('OuterSpoiler' + str(n - i + 1), parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))
        
        # old outer is new inner 
        outerEtaLE = innerEtaLE
        # new inner is min next to kink  
        innerEtaLE = spoilerOuterEta - outerSpan / span
        # The inner and outer Xsi coordinate of the leading edge are defined by the rear spar location and the sparOffset
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset
        
        spoilerPhi = calcPhiLESpoiler(outerEtaLE, innerEtaLE, outerXsiLE, innerXsiLE, parentWingVAMPzero, cpacsWing)
        deltaEta = sin(spoilerPhi) * spoilerChord
        deltaXsi = cos(spoilerPhi) * spoilerChord
        
        outerEtaTE = outerEtaLE - deltaEta / span
        outerXsiTE = outerXsiLE + deltaXsi / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE - deltaEta / span
        innerXsiTE = innerXsiLE + deltaXsi / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        # We do not want the spoiler to overlap the kink as the inner Spoilers will start here
        if innerEtaTE < etaKink:
            innerEtaTE = etaKink
            innerXsiTE = innerXsiLE + spoilerChord / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        mySpoilers.append(createSpoiler('OuterSpoiler1', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))

    #===============================================================================
    # Inner Spoilers 
    #===============================================================================
    deltaArea = spoilerArea - outerArea
    noExport = False
    if deltaArea <= 0.:
        log.warning('VAMPzero SPOILER: Outboard Spoiler area already exceeds the required spoiler area by: %s' % str(deltaArea))
        noExport = True

    calcArea = 0.
    maxInnerArea = (etaKink - etaFus) * span * spoilerChord
    if maxInnerArea >= deltaArea and noExport == False:
        innerSpan = 0.
        while True:
            innerSpan += .01
            oldArea = calcArea
            calcArea = innerSpan * spoilerChord
            
            # This is the break condition that should be hit normally
            if abs(deltaArea - calcArea) < 0.1:
                break
            
            if innerSpan > (etaKink - etaFus) * span:
                log.warning('VAMPzero SPOILER: The spoiler span of the inner spoiler exceeds the available span betweent fuselage and kink, continuing with calcArea = %s' % str(calcArea))
                break 
            if oldArea > calcArea:
                log.warning('VAMPzero SPOILER: Inner spoiler area apparently reached a maximum, continuing with calcArea = %s' % str(calcArea))
                break 

    elif noExport == False:
        log.warning('VAMPzero SPOILER: There is not sufficient space for the inner spoiler(s) between the kink and the fuselage!')
        spoilerChord = deltaArea / ((etaKink - etaFus) * span)
        innerSpan = (etaKink - etaFus) * span
        calcArea = deltaArea
        log.warning('VAMPzero SPOILER: The spoilerchord will be enlarged to %s!' % str(spoilerChord))
    
    if noExport == True:
        nInnerSpoiler = 0
        log.debug('VAMPzero SPOILER: Exporting %s Spoiler inside of the kink.' % (str(nInnerSpoiler)))
    else: 
        nInnerSpoiler = innerSpan ** 2 / (calcArea * 3.)
        log.debug('VAMPzero SPOILER: Exporting %s Spoiler inside of the kink for an area of %s m2.' % (str(nInnerSpoiler), str(calcArea)))
    
        

    #===========================================================================
    # 1 Spoiler
    #===========================================================================
    if nInnerSpoiler == 0:
        pass
    
    elif nInnerSpoiler <= 1:
        # The outer eta of the leading Edge to the eta of the kink
        outerEtaLE = etaKink
        # The inner eta of the leading edge is the outer eta minus the span of the inner spoiler 
        innerEtaLE = outerEtaLE - innerSpan / span
        # The outer Xsi at the leading Edge is defined by the sparLocation of the Kink
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        # The innner Xsi remains an absolute chord of the spoiler
        chordInnerSpoiler = (1-outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
        innerXsiLE = 1 - chordInnerSpoiler / calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing)
        
        # Eta Coordinates stay constant
        # Xsi Coordinates are shifted by spoilerChord
        outerEtaTE = outerEtaLE
        outerXsiTE = outerXsiLE + spoilerChord / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE
        innerXsiTE = innerXsiLE + spoilerChord / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        mySpoilers.append(createSpoiler('InnerSpoiler1', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))
    
    #===========================================================================
    # 2 Spoiler
    #===========================================================================
    elif nInnerSpoiler > 1. and nInnerSpoiler <= 2.:
        # First inner spoiler 
        # The outer eta of the leading Edge to the eta of the kink
        outerEtaLE = etaKink
        # The inner eta of the leading edge is the outer eta minus the span of the inner spoiler 
        innerEtaLE = outerEtaLE - innerSpan / span / 2.
        # The outer Xsi at the leading Edge is defined by the sparLocation of the Kink
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        # The innner Xsi remains an absolute chord of the spoiler
        chordInnerSpoiler = (1-outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
        innerXsiLE = 1 - chordInnerSpoiler / calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing)
        
        # Eta Coordinates stay constant
        # Xsi Coordinates are shifted by spoilerChord
        outerEtaTE = outerEtaLE
        outerXsiTE = outerXsiLE + spoilerChord / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE
        innerXsiTE = innerXsiLE + spoilerChord / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        mySpoilers.append(createSpoiler('InnerSpoiler2', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))
        
        # Second inner spoiler
        # old inner becomes new outer
        outerEtaLE = innerEtaLE
        # The inner eta of the leading edge is the outer eta minus the span of the inner spoiler 
        innerEtaLE = outerEtaLE - innerSpan / span / 2.
        # The outer Xsi at the leading Edge is defined by the sparLocation of the Kink
        outerXsiLE = xsiSpar_interp(outerEtaLE) + sparOffset
        # The innner Xsi remains an absolute chord of the spoiler
        chordInnerSpoiler = (1-outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
        innerXsiLE = 1 - chordInnerSpoiler / calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing)
        
        # Eta Coordinates stay constant
        # Xsi Coordinates are shifted by spoilerChord
        outerEtaTE = outerEtaLE
        outerXsiTE = outerXsiLE + spoilerChord / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
        innerEtaTE = innerEtaLE
        innerXsiTE = innerXsiLE + spoilerChord / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        mySpoilers.append(createSpoiler('InnerSpoiler1', parentWingVAMPzero.id, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE))

    #===========================================================================
    # Output to CPACS
    #===========================================================================
    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_spoilers()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_spoilers(spoilersType())
    
    log.debug('VAMPzero Spoiler: Exporting %s Spoilers to CPACS.' % (str(len(mySpoilers))))
    for spoiler in mySpoilers:
        cpacsComponentSegment.get_controlSurfaces().get_spoilers().add_spoiler(spoiler)


def calcPhiLESpoiler(outerEta, innerEta, outerXsi, innerXsi, myWing, cpacsWing):
    '''
    Calculates the angle phi of the leading edge of a spoiler given
    a combination of eta and xsi coordinates 
    '''
    span = myWing.span.getValue() / 2.
    phiLE = myWing.phiLE.getValue()
    
    deltaY = (outerEta - innerEta) * span

    absInnerX = innerXsi * calcChordLengthAtEta(innerEta, myWing, cpacsWing) + tan(phiLE * rad) * span * innerEta
    absOuterX = outerXsi * calcChordLengthAtEta(outerEta, myWing, cpacsWing) + tan(phiLE * rad) * span * outerEta
    deltaX = absOuterX - absInnerX
    
    phiSpoilerLE = atan(deltaX / deltaY)
    
    return phiSpoilerLE

    
def createSpoiler(name, parentUID, innerEtaLE, innerEtaTE, innerXsiLE, innerXsiTE, outerEtaLE, outerEtaTE, outerXsiLE, outerXsiTE):
    #===========================================================================
    # Header
    #===========================================================================
    log.debug('VAMPzero SPOILER: Creating Spoiler: %s' % (str(name)))
    log.debug('VAMPzero SPOILER: innerEtaLE: %s' % str(innerEtaLE))
    log.debug('VAMPzero SPOILER: innerEtaTE: %s' % str(innerEtaTE))
    log.debug('VAMPzero SPOILER: innerXsiLE: %s' % str(innerXsiLE))
    log.debug('VAMPzero SPOILER: innerXsiTE: %s' % str(innerXsiTE))
    log.debug('VAMPzero SPOILER: outerEtaLE: %s' % str(outerEtaLE))
    log.debug('VAMPzero SPOILER: outerEtaTE: %s' % str(outerEtaTE))
    log.debug('VAMPzero SPOILER: outerXsiLE: %s' % str(outerXsiLE))
    log.debug('VAMPzero SPOILER: outerXsiTE: %s' % str(outerXsiTE))
    
    myName = stringBaseType(None, None, None, name)
    myDescription = stringBaseType(None, None, None, 'spoiler from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, parentUID)

    myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.75)))
    innerBorder = controlSurfaceBorderSpoilerType(etaLE=doubleBaseType(valueOf_=str(innerEtaLE)), etaTE=doubleBaseType(valueOf_=str(innerEtaTE)), xsiLE=doubleBaseType(valueOf_=str(innerXsiLE)), xsiTE=doubleBaseType(valueOf_=str(innerXsiTE)), leadingEdgeShape=myleadingEdgeShape)
    outerBorder = controlSurfaceBorderSpoilerType(etaLE=doubleBaseType(valueOf_=str(outerEtaLE)), etaTE=doubleBaseType(valueOf_=str(outerEtaTE)), xsiLE=doubleBaseType(valueOf_=str(outerXsiLE)), xsiTE=doubleBaseType(valueOf_=str(outerXsiTE)), leadingEdgeShape=myleadingEdgeShape)
    
    myOuterShape = controlSurfaceOuterShapeSpoilerType(innerBorder=innerBorder, outerBorder=outerBorder)
    myStructure = wingComponentSegmentStructureType()
    mySpoiler = spoilerType(uID=name + 'UID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape, structure=myStructure)
    createSpoilerStructure(mySpoiler)
    return mySpoiler

def createSpoilerStructure(mySpoiler):
    myUID = mySpoiler.get_uID()

    
    createShell(mySpoiler, myUID, 'spoiler', thickness=0.005)
    createSpars(mySpoiler, myUID, 'spoiler')
    createRibs(mySpoiler, myUID, 'spoiler', thickness=0.001, nRibs=6)

