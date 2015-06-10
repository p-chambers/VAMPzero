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



def createRudder(parentVtpCPACS, parentVtpVAMPzero, myRudder):
    '''
    This is the main export method for the wings aileron
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentVtpVAMPzero.id + ']'
    cpacsVtp = getObjfromXpath(parentVtpCPACS, cpacsPath)
    cpacsComponentSegment = cpacsVtp.get_componentSegments().get_componentSegment()[0]

    #===========================================================================
    # Header
    #===========================================================================
    myName = stringBaseType(None, None, None, 'rudder')
    myDescription = stringBaseType(None, None, None, 'rudder from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, 'vtp_Cseg')
    
    #===========================================================================
    # Outer Shape
    # With the rudder this is pretty simple as it is supposed to cover
    # the same span as the VTP 
    #===========================================================================
    # the inner border eta is determined from the rooYLocation of the Rudder and the vtp span
    vtpSpan = parentVtpVAMPzero.span.getValue() / 2.
    innerEtaLE = 0.
    outerEtaLE = 1.
    
    innerXsiLE = myRudder.cRoot.getValue() / parentVtpVAMPzero.cRoot.getValue() 
    outerXsiLE = myRudder.cTip.getValue() / parentVtpVAMPzero.cTip.getValue()
    
    # start writing back
    myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.5)), xsiUpperSkin=doubleBaseType(valueOf_=str(0.85)), xsiLowerSkin=doubleBaseType(valueOf_=str(0.85)))
    innerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(innerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(innerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    outerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(outerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(outerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    
    myOuterShape = controlSurfaceOuterShapeTrailingEdgeType(innerBorder=innerBorder, outerBorder=outerBorder)

    cpacsRudder = trailingEdgeDeviceType(uID='rudderUID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape)

    createPath(cpacsRudder, 'rudder')

    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_trailingEdgeDevices(trailingEdgeDevicesType())
    
    cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices().add_trailingEdgeDevice(cpacsRudder)
    
    
