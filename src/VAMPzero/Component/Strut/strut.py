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
from VAMPzero.Component.Airfoil.airfoil import airfoil
from VAMPzero.Component.Strut.Geometry.active import active
from VAMPzero.Component.Strut.Geometry.depth import depth
from VAMPzero.Component.Strut.Geometry.etaStrut import etaStrut
from VAMPzero.Component.Strut.Mass.mStrut import mStrut
from VAMPzero.Component.Strut.Aerodynamic.cD0c import cD0c
from VAMPzero.Component.Wing.Aerodynamic.cfLAM import cfLAM
from VAMPzero.Component.Wing.Aerodynamic.cfTURB import cfTURB
from VAMPzero.Component.Wing.Aerodynamic.formFactor import formFactor
from VAMPzero.Component.Wing.Aerodynamic.nLam import nLam
from VAMPzero.Component.Wing.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Strut.Geometry.xTip import xTip
from VAMPzero.Component.Strut.Geometry.yTip import yTip
from VAMPzero.Component.Strut.Geometry.zTip import zTip

from VAMPzero.Component.Strut.Geometry.xRoot import xRoot
from VAMPzero.Component.Strut.Geometry.yRoot import yRoot
from VAMPzero.Component.Strut.Geometry.zRoot import zRoot

from VAMPzero.Component.Strut.Geometry.aspectRatio import aspectRatio
from VAMPzero.Component.Wing.Geometry.cMAC import cMAC
from VAMPzero.Component.Strut.Geometry.cRoot import cRoot
from VAMPzero.Component.Wing.Geometry.cTip import cTip
from VAMPzero.Component.Strut.Geometry.dihedral import dihedral

from VAMPzero.Component.Wing.Geometry.expArea import expArea
from VAMPzero.Component.Strut.Geometry.phi25 import phi25
from VAMPzero.Component.Strut.Geometry.phi50 import phi50
from VAMPzero.Component.Strut.Geometry.phiLE import phiLE
from VAMPzero.Component.Strut.Geometry.phiTE import phiTE
from VAMPzero.Component.Strut.Geometry.refArea import refArea
from VAMPzero.Component.Strut.Geometry.span import span
from VAMPzero.Component.Strut.Geometry.taperRatio import taperRatio
from VAMPzero.Component.Wing.Geometry.tcAVG import tcAVG
from VAMPzero.Component.Strut.Geometry.twist import twist
from VAMPzero.Component.Wing.Geometry.wetArea import wetArea
from VAMPzero.Component.Wing.Geometry.xMAC import xMAC
from VAMPzero.Component.Wing.Geometry.xMAC25 import xMAC25
from VAMPzero.Component.Wing.Geometry.yMAC import yMAC
from VAMPzero.Component.Wing.wing import wing
from VAMPzero.Handler.Component import component
from VAMPzero.Lib.CPACS.Export.Wing.wing import createWing
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD
from VAMPzero.Handler.Parameter import parameter

class strut(wing):
    '''
    class for the description of the strut as it would be included in a strut-braced wing design
    inherits component to throw errors and methods
    Component Class
    '''

    def __init__(self, aircraft):
        '''
        will initialize instance mainly used for documentation
        links to the aircraft instance
        initiates the airfoil class
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'strut'
        self.aircraft = aircraft
        self.level = 2

        # Mass
        self.mStrut = mStrut(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[4]/massDescription['+self.id+'_mass]/mass')
        self.parentUID = parameter(value=self.id, 
			cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[4]/massDescription['+self.id+'_mass]/parentUID')

        # Geometry
        self.refArea = refArea()
        self.expArea = expArea()
        self.wetArea = wetArea()
        self.aspectRatio = aspectRatio()
        self.span = span()
        self.depth = depth()
        self.active = active()
        self.taperRatio = taperRatio()
        self.tcAVG = tcAVG()
        self.cRoot = cRoot()
        self.cTip = cTip()
        self.cMAC = cMAC()
        self.yMAC = yMAC()
        self.xMAC = xMAC()
        self.xMAC25 = xMAC25()
        self.phiLE = phiLE()
        self.phiTE = phiTE()
        self.phi25 = phi25()
        self.phi50 = phi50()
        self.dihedral = dihedral()
        self.twist = twist()
        self.etaStrut = etaStrut()

        self.xRoot = xRoot()
        self.yRoot = yRoot()
        self.zRoot = zRoot()

        self.xTip = xTip()
        self.yTip = yTip()
        self.zTip = zTip()

        # Aerodynamics
        self.formFactor = formFactor()
        self.reynoldsNr = reynoldsNr()
        self.cfLAM = cfLAM()
        self.cfTURB = cfTURB()
        self.cD0c = cD0c()
        self.nLam = nLam()

        # Airfoil
        self.airfoilr = airfoil(self, position='root')
        self.airfoilt = airfoil(self, position='tip')


    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well.
        cpacsPath must be filled
        @author: Jonas Jepsen
        @param CPACSObj: the CPACS object holding the data for export
        '''
        if self.active.getValue():
            createWing(CPACSObj, id=self.id, zeroWing=self, LoD=WING_LOD.STRUT)
            super(wing, self).cpacsExport(CPACSObj)



####################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
####################################################################################################
