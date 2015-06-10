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
from math import pi, tan
from types import NoneType

from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath
from VAMPzero.Lib.CPACS.cpacs import stringBaseType, \
    controlSurfaceOuterShapeTrailingEdgeType, materialDefinitionType, \
    wingSkinType, wingStringerType, wingShellType, \
    wingComponentSegmentStructureType
from VAMPzero.Lib.CPACS.cpacs import stringUIDBaseType
from VAMPzero.Lib.CPACS.cpacs import controlSurfaceBorderTrailingEdgeType, leadingEdgeShapeType, \
    doubleBaseType, trailingEdgeDeviceType, controlSurfacesType, \
    trailingEdgeDevicesType
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Flap.Flap import calcChordLengthAtEta
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createShell, \
    createSpars, createRibs
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Path.path import createPath
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Track.track import createTracks
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Actuators.actuators import createActuators
import scipy.interpolate
from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.

def createAileron(parentWingCPACS, parentWingVAMPzero, myAileron):
    '''
    This is the main export method for the wings aileron
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentWingVAMPzero.id + ']'
    cpacsWing = getObjfromXpath(parentWingCPACS, cpacsPath)
    cpacsComponentSegment = cpacsWing.get_componentSegments().get_componentSegment()[0]

    #===========================================================================
    # Header
    #===========================================================================
    myName = stringBaseType(None, None, None, 'aileron')
    myDescription = stringBaseType(None, None, None, 'aileron from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, 'wing_Cseg')

    #===========================================================================
    # Initialization, i.e. fetching values throughout the code
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
    
    sparOffset = 0.1
    wingSpan = parentWingVAMPzero.span.getValue() / 2.
    #===========================================================================
    # Outer Shape
    #===========================================================================
    # The outer border eta station is set to 96 percent
    outerEtaLE = 0.96
    # The outer chord station is determined from the wing's chord at eta = 0.96
    # and the rear spar location + the spar offset
    outerXsiLE = xsiSpar_interp(0.96) + sparOffset
    outerWingChord = calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
    
    cTip = (1 - outerXsiLE) * outerWingChord
    
    # now we need to determine the necessary span for the aileron by gently increasing the span
    # this is an iterative process as the chord of the aileron is a function of the inbound span
    aileronArea = parentWingVAMPzero.aileron.refArea.getValue()
    delta = 0.01
    calcArea = 0.
    while abs(calcArea - aileronArea) > 0.1:
        if delta > outerEtaLE:
            parentWingVAMPzero.log.warning('VAMPzero EXPORT: Cannot determine the span of the aileron')
            parentWingVAMPzero.log.warning('VAMPzero EXPORT: aileronArea= '+str(aileronArea))
            parentWingVAMPzero.log.warning('VAMPzero EXPORT: Decreasing Spar Offset')
            sparOffset = sparOffset - 0.02
            delta = 0.01
            
        innerEtaLE = outerEtaLE - delta
        innerXsiLE = xsiSpar_interp(innerEtaLE) + sparOffset        
        innerWingChord = calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing)
        cRoot = (1 - innerXsiLE) * innerWingChord

        calcArea = (cTip + cRoot) / 2 * (outerEtaLE - innerEtaLE) * wingSpan
        delta += 0.005
 
    # start outer shape
    myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.5)), xsiUpperSkin=doubleBaseType(valueOf_=str(0.85)), xsiLowerSkin=doubleBaseType(valueOf_=str(0.85)))
    innerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(innerEtaLE)), etaTE=doubleBaseType(valueOf_=str(innerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(innerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    outerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(outerEtaLE)), etaTE=doubleBaseType(valueOf_=str(outerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(outerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    myOuterShape = controlSurfaceOuterShapeTrailingEdgeType(innerBorder=innerBorder, outerBorder=outerBorder)
    
    # structure
    myStructure = wingComponentSegmentStructureType()
    cpacsAileron = trailingEdgeDeviceType(uID='aileronUID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape, structure=myStructure)
    createAileronStructure(cpacsAileron)
    
    # Forward information about innerEtaLE to the flap
    parentWingVAMPzero.flap.maxEta = parameter(value=innerEtaLE, doc='This it the inner position of the aileron, the flap may not exceed it')
    
    # moveables
    deltaEta = outerEtaLE - innerEtaLE 
    innerParentXsi = xsiSpar_interp(innerEtaLE + 0.3 * deltaEta) + 0.02
    outerParentXsi = xsiSpar_interp(innerEtaLE + 0.7 * deltaEta) + 0.02

    createPath(cpacsAileron, 'aileron')
    createTracks(cpacsAileron, 'aileron')
    createActuators(cpacsAileron, 'aileron', [innerParentXsi, outerParentXsi])

    
    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_trailingEdgeDevices(trailingEdgeDevicesType())
    
    cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices().add_trailingEdgeDevice(cpacsAileron)
    
    
def createAileronStructure(myAileron):
    createShell(myAileron, 'aileronUID', 'aileron', thickness=0.001)
    createSpars(myAileron, 'aileronUID', 'aileron')
    createRibs(myAileron, 'aileronUID', 'aileron', thickness=0.001, pitch=0.25)
    
    
