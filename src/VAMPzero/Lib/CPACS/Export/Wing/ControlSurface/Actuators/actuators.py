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
from VAMPzero.Lib.CPACS.cpacs import doubleBaseType, stringBaseType, \
    materialDefinitionType, trackStructureType, controlSurfaceTrackTypeType, \
    actuatorParentAttachmentType, actuatorControlSurfaceAttachmentType, \
    actuatorAttachmentType, controlSurfaceActuatorType, stringUIDBaseType, \
    controlSurfaceActuatorsType

def createActuators(parent, typeOfSeg, parentXsi):
    actuators = []
    
    if typeOfSeg == 'aileron':
        # the actuators are located at 0.3 and 0.7 eta of the aileron. The actuator attaches to the upper part
        # of the aileron at a relative height of 0.8. 
        # On the controls surface side the actuator is located on the beginning 10%
        actuators.append(createActuator('aileron_actuator1', 'Aileron_Act1', 0.3, parentXsi[0], 0.8, parentXsi[0] + 0.1, 0.8))
        actuators.append(createActuator('aileron_actuator2', 'Aileron_Act2', 0.7, parentXsi[1], 0.8, parentXsi[1] + 0.1, 0.8))
        
    if len(actuators) != 0:
        parent.set_actuators(controlSurfaceActuatorsType(actuator=actuators))
        


def createActuator(uID='act', actuatorUID='Aileron_Act', etaControlSurface=0.3, parentXsi=0.7, parentHeight=0.1, controlSurfaceXsi=0.7, controlSurfaceHeight=0.1):
    #===============================================================================
    # Create the attachment 
    #===============================================================================
    etaControlSurface = doubleBaseType(valueOf_=str(etaControlSurface))
    material = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))

    parentXsi = doubleBaseType(valueOf_=str(parentXsi))
    parentHeight = doubleBaseType(valueOf_=str(parentHeight))
    parentAttachment = actuatorParentAttachmentType(parentXsi=parentXsi, parentHeight=parentHeight, material=material)

    parentXsi = doubleBaseType(valueOf_=str(controlSurfaceXsi))
    parentHeight = doubleBaseType(valueOf_=str(controlSurfaceHeight))
    controlSurfaceAttachment = actuatorControlSurfaceAttachmentType(parentXsi=parentXsi, parentHeight=parentHeight, material=material)
    
    attachment = actuatorAttachmentType(etaControlSurface=etaControlSurface, parentAttachment=parentAttachment, controlSurfaceAttachment=controlSurfaceAttachment)
    
    #===========================================================================
    # Create the actuator
    #===========================================================================
    
    return controlSurfaceActuatorType(uID=uID, actuatorUID=stringUIDBaseType(isLink='True', valueOf_=actuatorUID), attachment=attachment)
