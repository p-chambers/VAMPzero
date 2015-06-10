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

from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath
from VAMPzero.Lib.CPACS.cpacs import controlSurfacePathType, \
    controlSurfaceHingePointType, doubleBaseType, pointType, pointXZType, \
    controlSurfaceStepType, controlSurfaceStepsType
from types import NoneType

def createPath(parent, typeOfSeg='aileron', uID='controlSurface', innerX='0.', outerX='0.', innerHingeXsi='0.8', outerHingeXsi='0.8'):
    
    if typeOfSeg == 'aileron':
        innerHingeXsi = 0.75
        innerRelHeight = 0.2
        
        outerHingeXsi = 0.75
        outerRelHeight = 0.2
        steps = createStepsAileron()

    if typeOfSeg == 'elevator':
        innerHingeXsi = 0.75
        innerRelHeight = 0.2

        outerHingeXsi = 0.75
        outerRelHeight = 0.2
        steps = createStepsAileron()

    if typeOfSeg == 'stabilizer':
        innerHingeXsi = 0.25
        innerRelHeight = 0.5

        outerHingeXsi = 0.25
        outerRelHeight = 0.5
        steps = createStepsAileron()

    if typeOfSeg == 'rudder':
        innerHingeXsi = 0.75
        innerRelHeight = 0.2

        outerHingeXsi = 0.75
        outerRelHeight = 0.2
        steps = createStepsAileron()

    if typeOfSeg == 'flap' or typeOfSeg == 'innerFlap':
        innerHingeXsi = innerHingeXsi
        innerRelHeight = 0.5
        
        outerHingeXsi = outerHingeXsi
        outerRelHeight = 0.5
        steps = createStepsFlaps(innerX, outerX)

    if typeOfSeg == 'slat':
        innerHingeXsi = innerHingeXsi
        innerRelHeight = 0.5
        
        outerHingeXsi = outerHingeXsi
        outerRelHeight = 0.5
        steps = createStepsSlats(innerX, outerX)
        
        
    innerHinge = controlSurfaceHingePointType(hingeXsi=doubleBaseType(valueOf_=str(innerHingeXsi)), hingeRelHeight=doubleBaseType(valueOf_=str(innerRelHeight)))
    outerHinge = controlSurfaceHingePointType(hingeXsi=doubleBaseType(valueOf_=str(outerHingeXsi)), hingeRelHeight=doubleBaseType(valueOf_=str(outerRelHeight)))

    myPath = controlSurfacePathType(innerHingePoint=innerHinge, outerHingePoint=outerHinge, steps=steps)
    parent.set_path(myPath)

def createStep(deflection, x1, y1, z1, x2, z2, rotation):
    relDeflection = doubleBaseType(valueOf_=str(deflection))
    innerHingeTranslation = pointType(x=doubleBaseType(valueOf_=str(x1)), y=doubleBaseType(valueOf_=str(y1)) , z=doubleBaseType(valueOf_=str(z1)))
    outerHingeTranslation = pointXZType(x=doubleBaseType(valueOf_=str(x2)), z=doubleBaseType(valueOf_=str(z2)))
    hingeLineRotation = doubleBaseType(valueOf_=str(rotation))
    
    return controlSurfaceStepType(relDeflection=relDeflection, innerHingeTranslation=innerHingeTranslation, outerHingeTranslation=outerHingeTranslation, hingeLineRotation=hingeLineRotation)

def createStepsAileron():
    step1 = createStep(25, 0., 0., 0., 0., 0., 25.) 
    step2 = createStep(0, 0., 0., 0., 0., 0., 0.)
    step3 = createStep(-25, 0., 0., 0., 0., 0., -25.)
    
    steps = [step1, step2, step3]
    
    return controlSurfaceStepsType(step=steps)

def createStepsFlaps(innerX, outerX):
    step1 = createStep(0, 0., 0., 0., 0., 0., 0.)
    step2 = createStep(10, innerX / 2., 0., 0., outerX / 2., 0., 10.) 
    step3 = createStep(40, innerX, 0., 0., outerX, 0., 40.)
    
    steps = [step1, step2, step3]
    
    return controlSurfaceStepsType(step=steps)

def createStepsSlats(innerX, outerX):
    step1 = createStep(0, 0., 0., 0., 0., 0., 0.)
    step2 = createStep(30, -innerX, 0., 0., -outerX, 0., -30.) 
        
    steps = [step1, step2]
    
    return controlSurfaceStepsType(step=steps)
    