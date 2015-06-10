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

from math import pi,sin, sqrt,cos, tan

from VAMPzero.Lib.CPACS.cpacs import wingSectionsType, positioningsType
from VAMPzero.Lib.CPACS.Export.Wing.Shape.functions import createWingSection, createWingSegments
from VAMPzero.Lib.CPACS.Export.export import createPositioning

rad = pi / 180.


def createUCAVWing(myWing, id, cTip, cRoot, span, Sref, phiLE, dihedral, etakf, strUID):
    '''
    This method creates a ucav wing geometry in the 'myWing' parameter.
    @param myWing: wings CPACS object
    @param cTip: length of chord at wing tip [m]
    @param cRoot: length of chord at wing root [m]
    @param span: span of the wing [m]
    @param Sref: reference area [m^2]
    @param phiLE: sweep angle at the leading edge [deg]
    @param dihedral: dihedralangle of the wing [deg] 
    @param etakf: dimensionless span coordinate [-]
    @param strUID: 
    '''
    # sections and positionings will be created, all existing sections and positionings will be deleted
    mySections = wingSectionsType()
    myPositionings = positioningsType()
    # calc Lvl 1 parameters
    cRoot, cKink, cTip,etaD = calcWing(span, Sref, phiLE, etakf)
    createWingSection(mySections, 0.,0.,0., cRoot,1.,cRoot, 0.,0.,0., 'NACA0000', 1, strUID + '_Sec1', strUID + '_Sec1', strUID + '_Sec1')
    createWingSection(mySections, 0.,0.,0., cKink,1.,cKink, 0.,0.,0., 'NACA0000', 1, strUID + '_Sec2', strUID + '_Sec2', strUID + '_Sec2')
    createWingSection(mySections, 0.,0.,0., cTip,1.,cTip, 0.,0.,0., 'NACA0000', 1, strUID + '_Sec3', strUID + '_Sec3', strUID + '_Sec3')
    #Tip Section rather short
    createWingSection(mySections, 0.,0.,0., 0.01,1.,0.01, 0.,0.,0., 'NACA0000', 1, strUID + '_Sec4', strUID + '_Sec4', strUID + '_Sec4')
    # calc length from span, sweep and dihedral
    sweep_rad = phiLE/180. * pi
    dihedral_rad = dihedral/180. * pi
    length1 = (etakf*span/2.)/cos(sweep_rad)/cos(dihedral_rad)          # @todo: provide dihedral
    length2 = span/2.*(1-etakf-etaD)/cos(sweep_rad)/cos(dihedral_rad)        # @todo: provide dihedral
    length3 = span/2.*etaD/cos(sweep_rad)/cos(dihedral_rad)        # @todo: provide dihedral
    
    createPositioning(myPositionings,str(id) + '_Pos1',None, str(id) + '_Sec1',0.,0.,0.,id)
    createPositioning(myPositionings,str(id) + '_Pos2',str(id) + '_Sec1',str(id) + '_Sec2',length1,phiLE,dihedral,id)
    createPositioning(myPositionings,str(id) + '_Pos3',str(id) + '_Sec2',str(id) + '_Sec3',length2,phiLE,dihedral,id)
    createPositioning(myPositionings,str(id) + '_Pos4',str(id) + '_Sec3',str(id) + '_Sec4',length3,phiLE,dihedral,id)
    
    myWing.set_sections(mySections)
    myWing.set_positionings(myPositionings)

    createWingSegments(myWing, strUID, 3)

def calcWing(span, Sref, phiLE, etakf):
    '''
    This method calculates the 'missing' wing parameters.
    @param span: span of the wing [m]
    @param Sref: reference area [m^2]
    @param taperRatio: 
    @param phi: 
    @param etakf: dimensionless span coordinate [-]
    '''
    tk      = calctk(phiLE, span/2., etakf, Sref/2.)
    ti      = calcti(tk, etakf, phiLE, span/2.)
    etaD    = calcetaD(phiLE, tk, span/2.)
    ta      = tk
    #print ti,tk,ta, etaD
    return ti,tk,ta, etaD

def calctk(phiLE, span, etakf, Sref):
    phi = phiLE * rad
    t1 = 2 * sqrt(sin(phi))/cos(phi)
    t2 = sqrt(span**2*(etakf**2+1)*sin(phi)-cos(phi)*Sref )
    t3 = 2*span * tan(phi)
    return t3-t1*t2
    
def calcti(tk,etakf,phiLE, span):
    phi = phiLE * rad
    return tk + 2 * etakf * span /(tan(pi/2-phi))

def calcetaD(phiLE, tk, span):
    phi = phiLE * rad
    return tan(pi/2-phi)* tk /(2*span)