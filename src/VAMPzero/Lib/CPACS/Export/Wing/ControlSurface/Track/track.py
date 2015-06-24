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
    controlSurfaceTracksType, trackActuatorType, stringUIDBaseType

nFlapActuators = 1
    
def createTracks(parent, typeOfSeg='aileron', uID='controlSurfaceID'):
    tracks = []
    if typeOfSeg == 'aileron':
        tracks.append(createTrackAileron(uID + '_track_1', 0.25, 'trackType1'))
        tracks.append(createTrackAileron(uID + '_track_2', 0.75, 'trackType1'))

    if typeOfSeg == 'innerFlap':
        tracks.append(createTrackFlap(uID + '_track_1', 0.0, 'trackType3', 'trackSubType2'))
        tracks.append(createTrackFlap(uID + '_track_2', 0.66, 'trackType3'))

    if typeOfSeg == 'flap':
        tracks.append(createTrackFlap(uID + '_track_1', 0.275, 'trackType3'))
        tracks.append(createTrackFlap(uID + '_track_2', 0.725, 'trackType3'))
    
    if len(tracks) != 0:
        parent.set_tracks(controlSurfaceTracksType(track=tracks))
        


def createTrackAileron(uid, eta, trackType):
    eta = doubleBaseType(valueOf_=str(eta))
    trackType = stringBaseType(valueOf_=trackType)
    controlSurfaceAttachment = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    #parentAttachment = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    trackStructure = trackStructureType(controlSurfaceAttachment=controlSurfaceAttachment)
    return controlSurfaceTrackTypeType(uID=uid, eta=eta, trackType=trackType, trackStructure=trackStructure)


def createTrackFlap(uID, eta, trackType, trackSubType=None, actuatorcounter=1):
    eta = doubleBaseType(valueOf_=str(eta))
    trackType = stringBaseType(valueOf_=trackType)
    if trackSubType is not None:
        trackSubType = stringBaseType(valueOf_=trackSubType)
    
    global nFlapActuators
    trackActuator = trackActuatorType(uID=uID + '_actuatorUID', actuatorUID=stringUIDBaseType(isLink='true', valueOf_='Act_FT'+str(nFlapActuators)), material=materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001')))
    nFlapActuators += 1
    controlSurfaceAttachment = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    #parentAttachment = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    sidePanels = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    upperPanel = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    lowerPanel = materialDefinitionType(materialUID=stringBaseType(valueOf_='titan'), thickness=doubleBaseType(valueOf_='0.001'))
    rollerTrack = materialDefinitionType(materialUID=stringBaseType(valueOf_='titan'), thickness=doubleBaseType(valueOf_='0.001'))
    ribs = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    car = materialDefinitionType(materialUID=stringBaseType(valueOf_='aluminium2024'), thickness=doubleBaseType(valueOf_='0.001'))
    
    trackStructure = trackStructureType(controlSurfaceAttachment=controlSurfaceAttachment, sidePanels=sidePanels, upperPanel=upperPanel, lowerPanel=lowerPanel, rollerTrack=rollerTrack, ribs=ribs, car=car)
    
    if trackSubType is None:
        return controlSurfaceTrackTypeType(uID=uID, eta=eta, trackType=trackType, trackStructure=trackStructure, actuator=trackActuator)
    else:
        return controlSurfaceTrackTypeType(uID=uID, eta=eta, trackType=trackType, trackSubType=trackSubType, trackStructure=trackStructure, actuator=trackActuator)
