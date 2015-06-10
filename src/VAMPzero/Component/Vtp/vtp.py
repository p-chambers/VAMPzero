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
from VAMPzero.Component.Main.Parameter.uID import uID
from VAMPzero.Component.Vtp.Rudder.rudder import rudder
from VAMPzero.Component.Vtp.CoG.posCoG import posCoG
from VAMPzero.Component.Vtp.Geometry.LoD import LoD
from VAMPzero.Component.Vtp.Geometry.aspectRatio import aspectRatio
from VAMPzero.Component.Vtp.Geometry.cVT import cVT
from VAMPzero.Component.Vtp.Geometry.expArea import expArea
from VAMPzero.Component.Vtp.Geometry.lVT import lVT
from VAMPzero.Component.Vtp.Geometry.phi25 import phi25
from VAMPzero.Component.Vtp.Geometry.phi50 import phi50
from VAMPzero.Component.Vtp.Geometry.phiTE import phiTE
from VAMPzero.Component.Vtp.Geometry.refArea import refArea
from VAMPzero.Component.Vtp.Geometry.refAreaTakeOff import refAreaTakeOff
from VAMPzero.Component.Vtp.Geometry.refAreaLanding import refAreaLanding
from VAMPzero.Component.Vtp.Geometry.span import span
from VAMPzero.Component.Vtp.Geometry.taperRatio import taperRatio
from VAMPzero.Component.Vtp.Geometry.xMAC import xMAC
from VAMPzero.Component.Vtp.Geometry.xRoot import xRoot
from VAMPzero.Component.Vtp.Geometry.zRoot import zRoot
from VAMPzero.Component.Vtp.Mass.mVtp import mVtp
from VAMPzero.Component.Wing.Aerodynamic.cD0c import cD0c
from VAMPzero.Component.Wing.Aerodynamic.cLMAX import cLMAX
from VAMPzero.Component.Wing.Aerodynamic.cLalpha import cLalpha
from VAMPzero.Component.Wing.Aerodynamic.cfLAM import cfLAM
from VAMPzero.Component.Wing.Aerodynamic.cfTURB import cfTURB
from VAMPzero.Component.Wing.Aerodynamic.formFactor import formFactor
from VAMPzero.Component.Wing.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Wing.Geometry.cMAC import cMAC
from VAMPzero.Component.Vtp.Geometry.cRoot import cRoot
from VAMPzero.Component.Wing.Geometry.cTip import cTip
from VAMPzero.Component.Vtp.Geometry.phiLE import phiLE
from VAMPzero.Component.Wing.Geometry.tcAVG import tcAVG
from VAMPzero.Component.Wing.Geometry.wetArea import wetArea
from VAMPzero.Component.Wing.Geometry.yMAC import yMAC
from VAMPzero.Component.Wing.wing import wing
from VAMPzero.Handler.Component import component
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.Export.VTP.vtp import createVTP
from VAMPzero.Component.Wing.Aerodynamic.nLam import nLam


class vtp(wing):
    '''
    Class for the vertical tailplane it inherits the wing class 
    '''

    def __init__(self, aircraft):
        '''
        will initialize instance mainly used for documentation
        links to the aircraft instance
        initiates the airfoil class
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'vtp'
        self.aircraft = aircraft
        self.level = 2

        self.UID = uID(cpacsPath='/cpacs/toolspecific/vampZero/vtpUID')
		
        # Mass
        self.mVtp = mVtp(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[3]/massDescription['+self.id+'_mass]/mass')
        self.parentUID = parameter(value=self.id, 
			cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[3]/massDescription['+self.id+'_mass]/parentUID')

        # CoG
        self.posCoG = posCoG(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[3]/massDescription['+self.id+'_mass]/location/x')
		
        # Geometry
        self.refArea = refArea()
        self.refAreaTakeOff = refAreaTakeOff()
        self.refAreaLanding = refAreaLanding()
        self.expArea = expArea()
        self.wetArea = wetArea()
        self.aspectRatio = aspectRatio()
        self.span = span()
        self.taperRatio = taperRatio()
        self.tcAVG = tcAVG()
        self.cRoot = cRoot()
        self.cTip = cTip()
        self.cMAC = cMAC()
        self.yMAC = yMAC()
        self.xMAC = xMAC()
        self.phiLE = phiLE()
        self.phiTE = phiTE()
        self.phi25 = phi25()
        self.phi50 = phi50()
        self.xRoot = xRoot()
        self.zRoot = zRoot()
        self.lVT = lVT()
        self.cVT = cVT()
        self.LoD = LoD()

        # Aerodynamics
        self.cLalpha = cLalpha()
        self.cLMAX = cLMAX()
        self.formFactor = formFactor()
        self.reynoldsNr = reynoldsNr()
        self.cfLAM = cfLAM()
        self.cfTURB = cfTURB()
        self.cD0c = cD0c()
        self.nLam = nLam()

        # Airfoil
        self.airfoilr = airfoil(self)  # Root Airfoil
        self.airfoilt = airfoil(self)  # Tip  Airfoil

        # Rudder
        self.rudder = rudder(self)

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        cpacsPath must be filled
        @author: Jonas Jepsen
        @param CPACSObj: the CPACS object holding the data for export
        '''
        # self.LoD.setValue(1)    # level of detail [0,1]
        createVTP(CPACSObj, self.id, self.xRoot.getValue(), self.zRoot.getValue(), self.airfoilr.tc.getValue(), self.airfoilt.tc.getValue(), self.cRoot.getValue(),
                  self.cTip.getValue(), self.span.getValue(), self.phiLE.getValue(),  self.LoD.getValue())

        super(wing, self).cpacsExport(CPACSObj)

        ###################################################################################################

# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
