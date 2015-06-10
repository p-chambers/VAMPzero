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
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Path.path import createPath

from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath
from VAMPzero.Lib.CPACS.cpacs import stringBaseType
from VAMPzero.Lib.CPACS.cpacs import stringUIDBaseType
from VAMPzero.Lib.CPACS.cpacs import controlSurfaceOuterShapeTrailingEdgeType
from VAMPzero.Lib.CPACS.cpacs import controlSurfaceBorderTrailingEdgeType, leadingEdgeShapeType, \
    doubleBaseType, trailingEdgeDeviceType, controlSurfacesType, \
    trailingEdgeDevicesType

rad = pi / 180.



def createElevator(parentHtpCPACS, parentHtpVAMPzero, myElevator):
    '''
    This is the main export method for the htp elevator
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentHtpVAMPzero.id + ']'
    cpacsHtp = getObjfromXpath(parentHtpCPACS, cpacsPath)
    cpacsComponentSegment = cpacsHtp.get_componentSegments().get_componentSegment()[0]

    #===========================================================================
    # Header
    #===========================================================================
    myName = stringBaseType(None, None, None, 'elevator')
    myDescription = stringBaseType(None, None, None, 'elevator from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, parentHtpVAMPzero.id)
    
    #===========================================================================
    # Outer Shape
    #===========================================================================
    # the inner border eta is determined from the rooYLocation of the Elevator and the htp span
    htpSpan = parentHtpVAMPzero.span.getValue() / 2.
    innerEtaLE = myElevator.rootYLocation.getValue() / htpSpan
    
    # the inner border xsi is determined from the Root Chord and the Chord of the Htp at the location
    phiLE = parentHtpVAMPzero.phiLE.getValue()
    phiTE = parentHtpVAMPzero.phiTE.getValue()
    x1 = tan(phiLE * rad) * htpSpan * innerEtaLE
    x2 = tan(phiTE * rad) * htpSpan * innerEtaLE
    cInnerWing = (x2 + parentHtpVAMPzero.cRoot.getValue()) - x1
    innerXsiLE = 1 - (myElevator.cRoot.getValue() / cInnerWing)

    # The outer border eta station is set to the inner eta plus the span of the elevator
    outerEtaLE = innerEtaLE + myElevator.span.getValue() / htpSpan
    
    # The outer border xsi is determined in the same way as the inner border xsi
    x1 = tan(phiLE * rad) * htpSpan * outerEtaLE
    x2 = tan(phiTE * rad) * htpSpan * outerEtaLE
    cOuterWing = (x2 + parentHtpVAMPzero.cRoot.getValue()) - x1
    outerXsiLE = 1 - (myElevator.cTip.getValue() / cOuterWing)
    
    # start writing back
    myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.5)), xsiUpperSkin=doubleBaseType(valueOf_=str(0.85)), xsiLowerSkin=doubleBaseType(valueOf_=str(0.85)))
    innerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(innerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(innerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    outerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(outerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(outerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    
    myOuterShape = controlSurfaceOuterShapeTrailingEdgeType(innerBorder=innerBorder, outerBorder=outerBorder)

    cpacsElevator = trailingEdgeDeviceType(uID='elevatorUID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape)

    createPath(cpacsElevator, 'elevator')

    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_trailingEdgeDevices(trailingEdgeDevicesType())
    
    cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices().add_trailingEdgeDevice(cpacsElevator)


def createStabilizer(parentHtpCPACS, parentHtpVAMPzero, myElevator):
    '''
    This is the main export method for the stabilizer, i.e. the whole htp as control surface
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentHtpVAMPzero.id + ']'
    cpacsHtp = getObjfromXpath(parentHtpCPACS, cpacsPath)
    cpacsComponentSegment = cpacsHtp.get_componentSegments().get_componentSegment()[0]

    #===========================================================================
    # Header
    #===========================================================================
    myName = stringBaseType(None, None, None, 'stabilizer')
    myDescription = stringBaseType(None, None, None, 'stabilizer exported from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, parentHtpVAMPzero.id)

    #===========================================================================
    # Outer Shape
    #===========================================================================
    innerEtaLE = 0.
    innerXsiLE = 0.
    outerEtaLE = 1.
    outerXsiLE = 0.

    # start writing back
    #myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.5)), xsiUpperSkin=doubleBaseType(valueOf_=str(0.85)), xsiLowerSkin=doubleBaseType(valueOf_=str(0.85)))
    innerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(innerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(innerXsiLE)))
    outerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(outerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(outerXsiLE)))

    myOuterShape = controlSurfaceOuterShapeTrailingEdgeType(innerBorder=innerBorder, outerBorder=outerBorder)

    cpacsStabilizer = trailingEdgeDeviceType(uID='stabilizerUID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape)

    createPath(cpacsStabilizer, 'stabilizer')

    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_trailingEdgeDevices(trailingEdgeDevicesType())

    cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices().add_trailingEdgeDevice(cpacsStabilizer)
