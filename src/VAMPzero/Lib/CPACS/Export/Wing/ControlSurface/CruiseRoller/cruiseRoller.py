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
from VAMPzero.Lib.CPACS.cpacs import materialDefinitionType, stringBaseType, \
    doubleBaseType, cruiseRollerPositionType, blockedDOFType, booleanBaseType, \
    cruiseRollerType, cruiseRollersType

def createCruiseRollers(parent, typeOfSeg='outerFlap', uID='controlSurface'):
    rollers = []
    if typeOfSeg == 'outerFlap':
        rollers.append(createRoller(uID=uID))
        
    if len(rollers) > 0:
        parent.set_cruiseRollers(cruiseRollersType(cruiseRoller=rollers))


def createRoller(uID='cruiseRoller1UID', eta=0.02, xsi=0.05, relHeight=0.3, positiv="False", negativ="True"):
    position = cruiseRollerPositionType(eta=doubleBaseType(valueOf_=str(eta)), xsi=doubleBaseType(valueOf_=str(xsi)), relHeight=doubleBaseType(valueOf_=str(relHeight)))
    parentAttachment = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    controlSurfaceAttachment = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    blockedDOF = blockedDOFType(positive=booleanBaseType(valueOf_=positiv), negative=booleanBaseType(valueOf_=negativ))
    
    return cruiseRollerType(uID=uID, position=position, parentAttachment=parentAttachment, controlSurfaceAttachment=controlSurfaceAttachment, blockedDOF=blockedDOF)

