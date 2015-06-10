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

from math import pi, cos

from VAMPzero.Lib.CPACS.cpacs import wingSectionsType, positioningsType, doubleBaseType
from VAMPzero.Lib.CPACS.Export.Wing.Shape.functions import createWingSection, createWingSegments
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createComponentSegment, createSpars, createShell, createRibs, createTanks, createWingFuselageAttachment, createWingWingAttachment
from VAMPzero.Lib.CPACS.Export.export import createPositioning


def createStrut(myWing, id, tcRoot, tcTip, cTip, cRoot, span, phiLE, dihedral, twist, xRoot, yRoot, etaStrut, strUID):
    '''
    This method creates a trapezoid wing geometry in the 'myWing' parameter.
    @author: Jonas Jepsen
    @param myWing: wings CPACS object
    @param id: the VAMPzero-id of the wing 
    @param cTip: length of chord at wing tip [m]
    @param cRoot: length of chord at wing root [m]
    @param span: span of the wing [m]
    @param phiLE: sweep angle at the leading edge [deg]
    @param dihedral: dihedralangle of the wing [deg]
    @param twist: twist of the outer wing section [deg]
    @param strUID: the CPACS-uID of the wing
    '''
    # sections and positionings will be created, all existing sections and positionings will be deleted
    mySections = wingSectionsType()
    myPositionings = positioningsType()

    incidence_angle = 2.

    createWingSection(mySections, tcRoot / 0.09, 0., 0., 0., cRoot, 1., cRoot, 0., incidence_angle, 0., 'NACA0009', 1, strUID + '_Sec1', strUID + '_Sec1', strUID + '_Sec1')
    createWingSection(mySections, tcRoot / 0.09, 0., 0., 0., cRoot, 1., cRoot, dihedral, incidence_angle, 0., 'NACA0009', 1, strUID + '_Sec2', strUID + '_Sec2', strUID + '_Sec2')
    createWingSection(mySections, tcTip / 0.09, 0., 0., 0., cTip, 1., cTip, dihedral, incidence_angle, 0., 'NACA0009', 1, strUID + '_Sec3', strUID + '_Sec3', strUID + '_Sec3')

    createPositioning(myPositionings, str(id) + '_Pos1', None, str(id) + '_Sec1', 0., 0., 0., id)
    createPositioning(myPositionings, str(id) + '_Pos2', str(id) + '_Sec1', str(id) + '_Sec2', yRoot, 0., 0., id)
    createPositioning(myPositionings, str(id) + '_Pos3', str(id) + '_Sec2', str(id) + '_Sec3', span, phiLE, dihedral, id)

    myWing.set_sections(mySections)
    myWing.set_positionings(myPositionings)
    
    createWingSegments(myWing, strUID, 2)

    createComponentSegment(myWing, strUID, fromElement='_Sec2_Elem1')
    createRibs(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'strut', etaStrut=etaStrut)
    createSpars(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'strut')
    createShell(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'strut')

    createWingFuselageAttachment(myWing.get_componentSegments().get_componentSegment()[0], strUID, typeOfSeg='strut')
    createWingWingAttachment(myWing.get_componentSegments().get_componentSegment()[0], strUID, typeOfSeg='strut')

    # set wing x - position and twist
    myWing.get_transformation().get_translation().set_x(doubleBaseType(None, None, None, str(xRoot)))
    #myWing.get_transformation().get_translation().set_y(doubleBaseType(None, None, None, str(yRoot)))