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
from VAMPzero.Lib.CPACS.cpacs import controlSurfaceBorderLeadingEdgeType, \
    leadingEdgeShapeType, doubleBaseType, controlSurfacesType, \
    controlSurfaceOuterShapeLeadingEdgeType, stringBaseType, leadingEdgeDevicesType, \
    leadingEdgeDeviceType, stringUIDBaseType
from math import pi, ceil
from types import NoneType
from VAMPzero.Lib.Log.log import zeroLogger
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Path.path import createPath


rad = pi / 180.
log = zeroLogger('Slat')

def createSlats(parentWingCPACS, parentWingVAMPzero, mySlat):
    '''
    This is the main export method for the wing's slats
    It assumes a constant absolut chord for all slats.
    At the engine position a 5% span gap is included for the slats
    Slats end 5% prior to the wing tip
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentWingVAMPzero.id + ']'
    cpacsWing = getObjfromXpath(parentWingCPACS, cpacsPath)
    cpacsComponentSegment = cpacsWing.get_componentSegments().get_componentSegment()[0]
    mySlats = []
    
    #===========================================================================
    # Initialization, i.e. fetching values throughout the code
    #===========================================================================
    yFus = parentWingVAMPzero.yFuselage.getValue()
    span = parentWingVAMPzero.span.getValue() / 2.
    etaFus = yFus / span

    slatArea = mySlat.refArea.getValue()

    # The absolut chord of all slats is equal it is determined by the  
    # total slat area over the remaining span
    # the remaining span is the span minus the fuselage section minus 5% around the engine
    # and 5% at the tip
    cSlat = slatArea / ((1.0 - etaFus - 0.1) * span)
    
    if cSlat > calcChordLengthAtEta(etaFus, parentWingVAMPzero, cpacsWing) * 0.075:
        log.warning('VAMPzero SLAT: The slat chord is larger than 7.5% of the wing\'s chord at the fuselage intersection.')

    
    #===========================================================================
    # Inner Wing Slats
    # ----------------
    #
    # At first inner wing slats are defined. These do only extend up to the engine
    # a plus minus 2.5% span are reserved for the slats
    # Note the calculation is only valid for nEngine == 2
    # The aspect ratio of a slat should not be higher than 5.5    
    #===========================================================================
    etaEngine = parentWingVAMPzero.etaEngine.getValue()
    innerSpan = span * (etaEngine - 0.025 - etaFus)
    innerArea = innerSpan * cSlat
    nInnerSlats = innerSpan ** 2. / (innerArea * 5.5)
    log.debug('VAMPzero SLAT: Exporting %s Slats inside of the engine for an area of %s m2.' % (str(nInnerSlats), str(innerArea)))

    #===========================================================================
    # 1 Slat
    #===========================================================================
    if nInnerSlats <= 1.:
        # the inner border eta is located at the Fuselage
        innerEtaTE = etaFus
        innerXsiTE = cSlat / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)

        # the outer border eta is determined from the span of the outer flap
        outerEtaTE = etaFus + innerSpan / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        
        mySlats.append(createSlat('InnerSlat1', parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
    
    #===========================================================================
    # 2 Slats
    #===========================================================================
    elif nInnerSlats > 1. and nInnerSlats < 2.:
        # the inner border eta is located at the Fuselage
        innerEtaTE = etaFus
        innerXsiTE = cSlat / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)

        # the outer border eta is determined from the span of the outer flap
        outerEtaTE = etaFus + innerSpan / 2. / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5

        mySlats.append(createSlat('InnerSlat1', parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
        
        # new inner is the old outer 
        innerEtaLE = outerEtaTE
        innerXsiLE = outerXsiTE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaLE = etaFus + innerSpan / span
        outerXsiLE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5

        mySlats.append(createSlat('InnerSlat2', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, innerX=innerX, outerX=outerX))
    else:
        log.warning('VAMPzero EXPORT: Need more inner slats')

    #===========================================================================
    # Outer Wing Slats
    # ----------------
    #
    # Determine the number of remaining slats
    # The aspect ratio of a slat should not be higher than 5.5 
    #===========================================================================
    slatArea = slatArea - innerArea
    calcArea = 0.
    spanSlat = 0.
     
    while abs(calcArea - slatArea) > 0.5:
        spanSlat += .01
        calcArea = spanSlat * cSlat

    #===========================================================================
    # Determine the number of slats
    # The aspect ratio of a slats should not be higher than 5.5 
    #===========================================================================
    nSlats = spanSlat ** 2. / (slatArea * 5.5)
    log.debug('VAMPzero SLAT: Exporting %s Slats outboard of the engine for an area of %s m2.' % (str(nSlats), str(slatArea)))
    
    #===========================================================================
    # 1 Slat
    #===========================================================================
    if nSlats <= 1.:
        # the inner border eta is located at the Fuselage
        innerEtaTE = etaEngine + 0.025
        innerXsiTE = cSlat / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)

        # the outer border eta is determined from the span of the outer flap
        outerEtaTE = innerEtaTE + spanSlat / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5

        mySlats.append(createSlat('OuterSlat1', parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
    
    #===========================================================================
    # 2 Slats
    #===========================================================================
    elif nSlats > 1. and nSlats < 2.:
        # the inner border eta is located at the Fuselage
        innerEtaTE = etaEngine + 0.025
        innerXsiTE = cSlat / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)

        # the outer border eta is determined from the span of the outer flap
        outerEtaTE = innerEtaTE + spanSlat / 2. / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5

        mySlats.append(createSlat('OuterSlat1', parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
        
        # new inner is the old outer 
        innerEtaTE = outerEtaTE
        innerXsiTE = outerXsiTE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaTE = innerEtaTE + spanSlat / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5

        mySlats.append(createSlat('OuterSlat2', parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
    else:
    #===========================================================================
    # n Slats
    #===========================================================================
        # the inner border eta is located at the Fuselage
        n = int(ceil(nSlats))
        innerEtaTE = etaEngine + 0.025
        innerXsiTE = cSlat / calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing)
        
        # First Slat
        # the outer border eta is determined from the span of the outer flap
        outerEtaTE = innerEtaTE + spanSlat / n / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5

        mySlats.append(createSlat('OuterSlat1', parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
        
        for i in range(2, n):
            # new inner is the old outer 
            innerEtaTE = outerEtaTE
            innerXsiTE = outerXsiTE
            # the outer border eta is determined from the full span of the total outer flap
            outerEtaTE = innerEtaTE + spanSlat / n / span
            outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)
            
            #Slats extend 50% of their chord lenght
            innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
            outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
            
            mySlats.append(createSlat('OuterSlat' + str(i), parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))

        # Last Slat
        # new inner is the old outer 
        innerEtaTE = outerEtaTE
        innerXsiTE = outerXsiTE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaTE = innerEtaTE + spanSlat / n / span
        outerXsiTE = cSlat / calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing)

        #Slats extend 50% of their chord lenght
        innerX = innerXsiTE * calcChordLengthAtEta(innerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = outerXsiTE * calcChordLengthAtEta(outerEtaTE, parentWingVAMPzero, cpacsWing) * 0.5
        
        mySlats.append(createSlat('OuterSlat' + str(n), parentWingVAMPzero.id, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX=innerX, outerX=outerX))
    
    #===========================================================================
    # Output to CPACS
    #===========================================================================
    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_leadingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_leadingEdgeDevices(leadingEdgeDevicesType())
    
    log.debug('VAMPzero SLAT: Exporting %s Slats to CPACS.' % (str(len(mySlats))))
    for slat in mySlats:
        cpacsComponentSegment.get_controlSurfaces().get_leadingEdgeDevices().add_leadingEdgeDevice(slat)
    
    
def createSlat(name, parentUID, innerEtaTE, innerXsiTE, outerEtaTE, outerXsiTE, innerX, outerX):
    #===========================================================================
    # Header
    #===========================================================================
    log.debug('VAMPzero SLAT: Creating Slat: %s' % (str(name)))
    log.debug('VAMPzero SLAT: innerEtaTE: %s' % str(innerEtaTE))
    log.debug('VAMPzero SLAT: outerEtaTE: %s' % str(outerEtaTE))
    log.debug('VAMPzero SLAT: innerXsiTE: %s' % str(innerXsiTE))
    log.debug('VAMPzero SLAT: outerXsiTE: %s' % str(outerXsiTE))

    
    myName = stringBaseType(None, None, None, name)
    myDescription = stringBaseType(None, None, None, 'slat from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, parentUID)

    myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.5)), xsiUpperSkin=doubleBaseType(valueOf_=str(0.85)), xsiLowerSkin=doubleBaseType(valueOf_=str(0.85)))
    innerBorder = controlSurfaceBorderLeadingEdgeType(etaLE=doubleBaseType(valueOf_=str(innerEtaTE)), xsiTEUpper=doubleBaseType(valueOf_=str(innerXsiTE)), xsiTELower=doubleBaseType(valueOf_=str(0.02)), leadingEdgeShape=myleadingEdgeShape)
    outerBorder = controlSurfaceBorderLeadingEdgeType(etaLE=doubleBaseType(valueOf_=str(outerEtaTE)), xsiTEUpper=doubleBaseType(valueOf_=str(outerXsiTE)), xsiTELower=doubleBaseType(valueOf_=str(0.02)), leadingEdgeShape=myleadingEdgeShape)
    
    myOuterShape = controlSurfaceOuterShapeLeadingEdgeType(innerBorder=innerBorder, outerBorder=outerBorder)
    
    mySlat = leadingEdgeDeviceType(uID=name + 'UID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape)
    createPath(mySlat, typeOfSeg = "slat", uID=name + 'UID', innerX=innerX, outerX=outerX, innerHingeXsi = 0.5, outerHingeXsi = 0.5)
    return mySlat

