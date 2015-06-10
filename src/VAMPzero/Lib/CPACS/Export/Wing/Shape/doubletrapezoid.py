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

from math import pi, cos, tan

from VAMPzero.Lib.CPACS.cpacs import wingSectionsType, positioningsType, doubleBaseType
from VAMPzero.Lib.CPACS.Export.Wing.Shape.functions import createWingSection, createWingSegments
from VAMPzero.Lib.CPACS.Export.export import createPositioning
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createComponentSegment


def createDoubleTrapezoidWing(myWing, id, cTip, cRoot, span, Sref, phiLE, dihedral, twist, xMAC25, etakf, strUID):
    '''
    This method creates a double trapezoid wing geometry in the 'myWing' parameter.
    @author: Jonas Jepsen
    @param myWing: wings CPACS object
    @param id: the VAMPzero-id of the wing 
    @param cTip: length of chord at wing tip [m]
    @param cRoot: length of chord at wing root [m]
    @param span: span of the wing [m]
    @param Sref: reference area [m^2]
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
    taperRatio = (cTip/cRoot)
    cRoot, cKink, cTip = calcWing(span, Sref, taperRatio, phiLE, etakf)
    createWingSection(mySections, 0.,0.,0., cRoot,1.,cRoot, 0.,0.,0., 'NACA653218', 1, strUID + '_Sec1', strUID + '_Sec1', strUID + '_Sec1')
    createWingSection(mySections, 0.,0.,0., cKink,1.,cKink, 0.,0.,0., 'NACA653218', 1, strUID + '_Sec2', strUID + '_Sec2', strUID + '_Sec2')
    createWingSection(mySections, 0.,0.,0., cTip,1.,cTip, 0.,twist,0., 'NACA653218', 1, strUID + '_Sec3', strUID + '_Sec3', strUID + '_Sec3')

    # calc length from span, sweep and dihedral
    sweep_rad = phiLE/180. * pi
    dihedral_rad = dihedral/180. * pi
    length1 = (etakf*span/2.)/cos(sweep_rad)/cos(dihedral_rad)
    length2 = span/2.*(1-etakf)/cos(sweep_rad)/cos(dihedral_rad)
    
    createPositioning(myPositionings,str(id) + '_Pos1',None, str(id) + '_Sec1',0.,0.,0.,id)
    createPositioning(myPositionings,str(id) + '_Pos2',str(id) + '_Sec1',str(id) + '_Sec2',length1,phiLE,dihedral,id)
    createPositioning(myPositionings,str(id) + '_Pos3',str(id) + '_Sec2',str(id) + '_Sec3',length2,phiLE,dihedral,id)
    
    myWing.set_sections(mySections)
    myWing.set_positionings(myPositionings)

    createWingSegments(myWing, strUID, 2)
    
    createComponentSegment(myWing, strUID)

    # calc wing position
    tauk = cTip/cKink
    myLambda = span**2/Sref
    sweep_rad = 35./180.*pi
    tanPhi25a = calcPhi25a(sweep_rad, taperRatio, tauk, etakf, span, cRoot)
    tanPhi25i = calcPhi25i(sweep_rad, taperRatio, tauk, etakf, span, cRoot)
    Xef = calcXef(cRoot, myLambda, tanPhi25i, tanPhi25a, etakf, taperRatio, tauk)
    xRoot = calcXRoot(xMAC25, Xef, cRoot)
    # set wing x - position
    myWing.get_transformation().get_translation().set_x(doubleBaseType(None, None, None,str(xRoot)))

def calcWing(span, Sref, taperRatio, phiLE, etakf):
    '''
    This method calculates the 'missing' wing parameters.
    @author: Jonas Jepsen
    @param span: span of the wing [m]
    @param Sref: reference area [m^2]
    @param taperRatio: taper ratio [-]
    @param phiLE: sweep angle at the leading edge [deg]
    @param etakf: dimensionless span coordinate [-]
    '''
    tauK = calcTauKink(span, etakf, Sref, taperRatio, phiLE)
    ti = calcTi(span, etakf, taperRatio, phiLE, tauK)
    ta = taperRatio * ti
    tk = ta / tauK
    return ti,tk,ta

def calcTi(bf, etakf, taperRatio, phiLE, tauK):
    '''
    @author: Jonas Jepsen
    @param bf: span of the wing [m]
    @param etakf: dimensionless span coordinate [-]
    @param taperRatio: taper ratio [-]
    @param phiLE: sweep angle at the leading edge [deg]
    @param tauK: ratio from chord length at tip over kink [-]
    @return: chord length at root [m]
    
    @note: this function is implemented with span and not aspect ratio because it simplifies the equation
    '''
    phi = phiLE/180. *pi
    ti = (1/2.)*tauK*etakf*bf*tan(phi)/(tauK-taperRatio)
    return ti

def calcTauKink(bf, etakf, S, taperRatio, phiLE):
    '''
    @author: Jonas Jepsen
    @param bf: span of the wing [m]
    @param etakf: dimensionless span coordinate [-]
    @param S: reference area [m^2]
    @param taperRatio: taper ratio [-]
    @param phiLE: sweep angle at the leading edge [deg]
    @return: ratio from chord length at tip over kink [-]
    
    @note: this function is implemented with span and not aspect ratio because it simplifies the equation
    '''
    phi = phiLE/180. *pi
    tauK = taperRatio*(4*S+bf**2*etakf*tan(phi))/(4*S-bf**2*etakf**2*tan(phi)+bf**2*etakf**2*tan(phi)*taperRatio-bf**2*etakf*tan(phi)*taperRatio)
    return tauK

def calcXef(Ti, Lambda, tanPhi25i, tanPhi25a, eta_k, tau_f, tau_k):
    '''
    This function calculates the translation of the t/4 line for the aerodynamic-rectangular wing.
    @param Ti: chord length at root [m]
    @param Lambda: aspect ratio [-]
    @param tanPhi25i: tangent of the sweep of the inner trapezoid's quarter chord line [-]
    @param phi25a: tangent of the sweep of the outer trapezoid's quarter chord line [-]
    @param eta_k: dimensionless span coordinate of kink [-]
    @param tau_f: taper ratio [-]
    @param tau_k: ratio from chord length at tip over kink [-]
    @return: the translation Xef
    '''
    part1 = eta_k**2*(1-tau_f*(3+1./tau_k)+tau_f*(2+1./tau_k)*tanPhi25a/tanPhi25i)
    part2 = eta_k*(3*tau_f*(1+1./tau_k)-2*tau_f*(2+1./tau_k)*tanPhi25a/tanPhi25i)
    part3 = tau_f*(2+1./tau_k)*tanPhi25a/tanPhi25i
    #print part1, part2, part3
    Xef = Ti*Lambda/12.*tanPhi25i*(part1 + part2 + part3)
    return Xef

def calcPhi25a(phiLE, tau_f, tau_k, eta_k, span, Ti):
    '''
    calcs the tan(sweep) of the outer wing at t/4 
    this function takes [rad] and returns [rad]
    @author: Jonas Jepsen
    @param phiLE: sweep angle at the leading edge [deg] 
    @param tau_f: taper ratio [-]
    @param tau_k: ratio from chord length at tip over kink [-]
    @param eta_k: dimensionless span coordinate of kink [-]
    @param span: span of the wing [m]
    @param Ti: chord length at root [m]
    @return: phi25a
    '''
    tanPhi25a = tan(phiLE)+ 1./4. * (tau_f-tau_f/tau_k)/(1.-eta_k)*2*Ti/span
    return tanPhi25a

def calcPhi25i(phiLE, tau_f, tau_k, eta_k, span, Ti):
    '''
    calcs the tan(sweep) of the inner wing at t/4
    this function takes [rad] and returns [rad]
    @author: Jonas Jepsen
    @param phiLE: sweep angle at the leading edge [deg] 
    @param tau_k: ratio from chord length at tip over kink [-]
    @param tau_f: taper ratio [-]
    @param eta_k: dimensionless span coordinate of kink [-]
    @param span: span of the wing [m]
    @param Ti: chord length at root [m]
    @return: phi25i
    '''
    tanPhi25i = tan(phiLE)+ 1./4. * (tau_f/tau_k-1)/eta_k*2*Ti/span
    return tanPhi25i

def calcXRoot(xMAC, Xef, Ti):
    '''
    this function calculates the x-position of the wing (leading edge at root)
    @author: Jonas Jepsen
    @param xMAC: x coordinate of wings mean aerodynamic chord
    @param Xef:  translation of the aerodynamic wing's quarter chord to wing's quarter chord (see Heinze script for definition)
    @param Ti: chord length at root [m]
    @return: xRoot.py, the wings x-position
    '''
    xRoot = xMAC - Xef-0.25*Ti
    return xRoot