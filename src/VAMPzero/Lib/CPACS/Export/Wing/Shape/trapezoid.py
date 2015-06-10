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

from VAMPzero.Lib.CPACS.cpacs import wingSectionsType, positioningsType
from VAMPzero.Lib.CPACS.Export.Wing.Shape.functions import createWingSection, createWingSegments
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createComponentSegment, createSpars, createShell, \
    createRibs
from VAMPzero.Lib.CPACS.Export.export import createPositioning


def createTrapezoidWing(myWing, id, tcRoot, tcTip, cTip, cRoot, span, phiLE, dihedral, twist, strUID):
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
    
    createWingSection(mySections, tcRoot / 0.09, 0., 0., 0., cRoot, 1., cRoot, 0., 0., 0., 'NACA0009', 1, strUID + '_Sec1', strUID + '_Sec1', strUID + '_Sec1')
    createWingSection(mySections, tcTip / 0.09, 0., 0., 0., cTip, 1., cTip, 0., twist, 0., 'NACA0009', 1, strUID + '_Sec2', strUID + '_Sec2', strUID + '_Sec2')
    # calc length from span, sweep and dihedral
    sweep_rad = phiLE / 180. * pi
    dihedral_rad = dihedral / 180. * pi
    length = (span / 2.) / cos(sweep_rad) / cos(dihedral_rad)  # @todo: provide dihedral
    
    createPositioning(myPositionings, str(id) + '_Pos1', None, str(id) + '_Sec1', 0., 0., 0., id)
    createPositioning(myPositionings, str(id) + '_Pos2', str(id) + '_Sec1', str(id) + '_Sec2', length, phiLE, dihedral, id)

    myWing.set_sections(mySections)
    myWing.set_positionings(myPositionings)
    
    createWingSegments(myWing, strUID, 1)

    createComponentSegment(myWing, strUID)
    createSpars(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'trapezoid')
    createShell(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'trapezoid')
    createRibs(parent=myWing.get_componentSegments().get_componentSegment()[0], parentUID=id, typeOfSeg='trapezoid')
