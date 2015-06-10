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

from math import pi, cos, tan, sqrt

from VAMPzero.Lib.CPACS.cpacs import wingSectionsType, positioningsType, doubleBaseType
from VAMPzero.Lib.CPACS.Export.Wing.Shape.functions import createWingSection, createWingSegments
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createComponentSegment, createSpars, createShell, createTanks, createRibs, \
    createWingFuselageAttachment
from VAMPzero.Lib.CPACS.Export.export import createPositioning
from numpy.ma.core import ceil


def createAdvDoubleTrapezoidWing(myWing, id, cTip, cRoot, span, Sref, dfus, phiLE, dihedral, twist, xMAC25, etakf, strUID, yfus, xRoot, etaEng, tcRoot, tcTip):
    '''
    This method creates a double trapezoid wing geometry in the 'myWing' parameter.
    
    ** Introduced a linear twist distribution from *0* at root to *twist* at tip 
    
    
    @author: Jonas Jepsen
    @param myWing: wings CPACS object
    @param id: the VAMPzero-id of the wing 
    @param cTip: length of chord at wing tip [m]
    @param cRoot: length of chord at wing root [m]
    @param span: span of the wing [m]
    @param Sref: reference area [m^2]
    @param dfus: fuselage diameter [m]
    @param phiLE: sweep angle at the leading edge [deg]
    @param dihedral: dihedralangle of the wing [deg]
    @param twist: twist of the outer wing section [deg]     
    @param etakf: dimensionless span coordinate [-]
    @param strUID: the CPACS-uID of the wing
    '''
    # sections and positionings will be created, all existing sections and positionings will be deleted
    mySections = wingSectionsType()
    myPositionings = positioningsType()
    # calc Lvl 1 parameters
    taperRatio = (cTip / cRoot)
    cRoot, cKink, cTip = calcWing(span, Sref, taperRatio, phiLE, etakf, dfus)

    # calc length from span, sweep and dihedral
    sweep_rad = phiLE / 180. * pi
    dihedral_rad = dihedral / 180. * pi
    # trying to correct the commented statement that uses dfus. will try to use yfus
    # length1 = dfus / 2.
    length1 = yfus
    length2 = (etakf * span / 2. - length1) / cos(sweep_rad) / cos(dihedral_rad)
    length3 = span / 2.*(1 - etakf) / cos(sweep_rad) / cos(dihedral_rad)
    
    # Increase (or reduce the twist by 4deg as that is the overall angle of incidence of the wing)
    twist = twist - 4.
    twistgrad = twist / (span / 2.)
    twist1 = twistgrad * length1 
    twist2 = twistgrad * etakf * (span / 2.)
    twist3 = twist
    
    createWingSection(mySections, tcRoot / 0.09, 0., 0., 0., cRoot, 1., cRoot, 0., 0., 0., 'NACA0009', 1, strUID + '_Sec1', strUID + '_Sec1', strUID + '_Sec1')
    createWingSection(mySections, tcRoot / 0.18, 0., 0., 0., cRoot, 1., cRoot, 0., 0., 0., 'NACA653218', 1, strUID + '_Sec2', strUID + '_Sec2', strUID + '_Sec2')
    createWingSection(mySections, tcTip / 0.18, 0., 0., 0., cKink, 1., cKink, 0., twist2, 0., 'NACA653218', 1, strUID + '_Sec3', strUID + '_Sec3', strUID + '_Sec3')
    createWingSection(mySections, tcTip / 0.18, 0., 0., 0., cTip, 1., cTip, 0., twist3, 0., 'NACA653218', 1, strUID + '_Sec4', strUID + '_Sec4', strUID + '_Sec4')

    createPositioning(myPositionings, str(id) + '_Pos1', None, str(id) + '_Sec1', 0., 0., 0., id)
    createPositioning(myPositionings, str(id) + '_Pos2', str(id) + '_Sec1', str(id) + '_Sec2', length1, 0., 0., id)
    createPositioning(myPositionings, str(id) + '_Pos3', str(id) + '_Sec2', str(id) + '_Sec3', length2, phiLE, dihedral, id)
    createPositioning(myPositionings, str(id) + '_Pos4', str(id) + '_Sec3', str(id) + '_Sec4', length3, phiLE, dihedral, id)
    
    myWing.set_sections(mySections)
    myWing.set_positionings(myPositionings)

    createWingSegments(myWing, strUID, 3)
    
    createComponentSegment(myWing, strUID)
    etafus = yfus / (span / 2.)
    # Ribs outboard of the Fuselage section are placed at 0.8 m distance
    nouterRibs = int(ceil((0.95 - etafus - 0.05) * span / 2. / 0.8))
    createRibs(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'advDoubletrapezoid', etaFus=etafus, nRibs=nouterRibs, etaEng=etaEng, span=span / 2.)
    createSpars(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'advDoubletrapezoid', length1 / (span / 2.), etakf / cos(dihedral_rad), cTip=cTip, cRoot=cRoot)
    createShell(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'advDoubletrapezoid')
    createWingFuselageAttachment(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'advDoubletrapezoid')
    
    # Estimate ribNum of outer Rib
    iRib = int(span * (0.85 - etaEng) / (2 * 0.8)) - 1
    createTanks(myWing.get_componentSegments().get_componentSegment()[0], strUID, 'advDoubletrapezoid', nRib=iRib)
    
    
    # calc wing position
    tauK = cTip / cKink
    etar = dfus / span
    # XN25F = calcXN25F(cRoot, span, phiLE, etar, etakf, tauK, taperRatio)
    # xRoot.py = calcXRoot(xMAC25, XN25F)
    
    # set wing x - position and twist
    myWing.get_transformation().get_translation().set_x(doubleBaseType(None, None, None, str(xRoot)))
    myWing.get_transformation().get_rotation().set_y(doubleBaseType(None, None, None, str(4.)))

def calcWing(span, Sref, taperRatio, phiLE, etakf, dfus):
    '''
    This method calculates the 'missing' wing parameters.
    @author: Jonas Jepsen
    @param span: span of the wing [m]
    @param Sref: reference area [m^2]
    @param taperRatio: the wings taper ratio
    @param phiLE: sweep angle of the leading edge [deg]
    @param etakf: dimensionless span coordinate [-]
    @param dfus: fuselage diameter [m]
    @return: chord at root, kink and tip
    '''
    etar = dfus / span
    Lambda = (span ** 2) / Sref
    tauK = calcTauKink(Lambda, etakf, etar, taperRatio, phiLE)
    ti = calcTi(Lambda, etakf, etar, Sref, taperRatio, phiLE, tauK)
    ta = taperRatio * ti
    tk = ta / tauK
    return ti, tk, ta

def calcTi(Lambda, etakf, etar, Sref, taperRatio, phiLE, tauK):
    '''
    @author: Jonas Jepsen
    @param Lambda: aspect ratio [-]
    @param etakf: dimensionless span coordinate of kink [-]
    @param etar: dimensionless span coordinate of wing-fuselage-intersection [-]
    @param Sref: reference area [m^2]
    @param phiLE: sweep angle at the leading edge [deg] 
    @param tauK: ratio from chord length at tip over kink [-]
    @return: chord length at root
    '''
    phi = phiLE / 180. *pi
    num = (-4 - Lambda * tan(phi) * etakf + Lambda * tan(phi) * etar + tan(phi) * Lambda * etakf * etar - tan(phi) * Lambda * etar ** 2) * sqrt(Lambda * Sref)
    den = (taperRatio * etakf - etakf - taperRatio - 1) * Lambda * 2
    ti = num / den
    return ti

def calcTauKink(Lambda, etakf, etar, taperRatio, phiLE):
    '''
    @author: Jonas Jepsen
    @param Lambda: aspect ratio [-]
    @param etakf: dimensionless span coordinate of kink [-]
    @param etar: dimensionless span coordinate of wing-fuselage-intersection [-]
    @param taperRatio: taper ratio [-]
    @param phiLE: sweep angle at the leading edge [deg] 
    @return: ratio from chord length at tip over kink [-]
    '''
    phi = phiLE / 180. *pi
    num = -taperRatio * (-4 - Lambda * tan(phi) * etakf + Lambda * tan(phi) * etar + tan(phi) * Lambda * etakf * etar - tan(phi) * Lambda * etar ** 2)
    den = (tan(phi) * Lambda * taperRatio * etakf ** 2 - Lambda * tan(phi) * taperRatio * etakf - tan(phi) * Lambda * taperRatio * etakf * etar + Lambda * tan(phi) * taperRatio * etar + 4 - tan(phi) * Lambda * etakf ** 2 + tan(phi) * Lambda * etar ** 2)
    tauK = num / den
    return tauK

def calcSref(Ti, span, etak, etar, tauk, tauf):
    '''
    used only for debugging purposes
    @author: Jonas Jepsen
    @param Ti: chord length at root [m]
    @param span: span of the wing [m]
    @param etak: dimensionless span coordinate of kink [-]
    @param etar: dimensionless span coordinate of wing-fuselage-intersection [-]
    @param tauk: ratio from chord length at tip over kink [-]
    @param tauf: taper ratio [-]
    @return: Sref (reference area)
    '''
    Sref = -0.5 * Ti * span * (-tauk * etar - etak * tauk + tauf * etar - tauf - tauf * tauk + tauf * etak * tauk) / tauk
    return Sref

def calcXN25F(Ti, span, phiLE, etar, etak, tauk, tauf):
    '''
    @author: Jonas Jepsen
    @param Ti: chord length at root [m]
    @param span: span of the wing [m]
    @param phiLE: sweep angle at the leading edge [deg] 
    @param etar: dimensionless span coordinate of wing-fuselage-intersection [-]
    @param etak: dimensionless span coordinate of kink [-]
    @param tauk: ratio from chord length at tip over kink [-]
    @param tauf: taper ratio [-]
    @return: XN25F
    '''
    phirad = phiLE / 180. * pi
    Ta = tauf * Ti
    Tk = Ta / tauk
    numpart1 = -1 * (Ti ** 2) * etar - 3 * Ti * Ta + Ti * tauk * Ta * etak - 2 * tan(phirad) * span * etak * Tk + 2 * tan(phirad) * span * (etak ** 2) * Ta - Ti * tauf * Ta * etak - (Ti ** 2) * tauk * etak + 4 * Ti * etar * Tk + 2 * Ti * Tk * etak - 2 * etar * (Ti ** 2) * tauk - 2 * tan(phirad) * span * (etak ** 2) * Ti - 2 * etak * Ti * tauf * Tk + 2 * tan(phirad) * span * Ta * etak + 2 * tan(phirad) * span * etak * etar * Tk - 2 * tan(phirad) * span * etar * Ti * etak - 2 * (Ti ** 2) * etak - 3 * Ti * Tk - 2 * Ti * tauf * Ta
    numpart2 = -2 * tan(phirad) * span * Tk + 2 * Ti * tauk * Ta + 3 * Ti * Ta * etak - 4 * tan(phirad) * span * Ta - Ti * tauk * etar * Tk + 8 * tan(phirad) * span * Ti * (etar ** 2) + 4 * tan(phirad) * span * (etar ** 2) * Tk + 2 * Ti * tauk * Tk - 2 * Ti * tauf * Tk
    num = (numpart1 + numpart2) * tauk
    den = 12 * Ti * (-1 * etar * tauk - tauk * etak + tauf * etar - tauf - tauf * tauk + tauf * tauk * etak)
    XN25F = num / den
    return XN25F

def calcXRoot(xMAC, XN25F):
    '''
    this function calculates the x-position of the wing (leading edge at root)
    @author: Jonas Jepsen
    @param xMAC: x coordinate of wings mean aerodynamic chord
    @param XN25F: translation of the aerodynamic wing's quarter chord to wing's leading edge(see Heinze script for definition)
    @return: xRoot.py, the wings x-position
    '''
    xRoot = xMAC - XN25F
    return xRoot
