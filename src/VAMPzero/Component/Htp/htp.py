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
from cmath import tan, pi

from VAMPzero.Component.Airfoil.airfoil import airfoil
from VAMPzero.Component.Htp.Aerodynamic.detadalpha import detadalpha
#from VAMPzero.Component.Htp.Aerodynamic.cLMIN import cLMIN
from VAMPzero.Component.Htp.Aerodynamic.cLMAXht import cLMAXht
from VAMPzero.Component.Htp.Aerodynamic.DPR import DPR
from VAMPzero.Component.Htp.Aerodynamic.CLalphaHTP_TO import CLalphaHTP_TO
from VAMPzero.Component.Htp.Aerodynamic.CLalphaHTP_CR import CLalphaHTP_CR
from VAMPzero.Component.Htp.Aerodynamic.CLalphaHTP_L import CLalphaHTP_L
from VAMPzero.Component.Htp.CoG.posCoG import posCoG
from VAMPzero.Component.Htp.Geometry.LoD import LoD
from VAMPzero.Component.Htp.Geometry.aspectRatio import aspectRatio
from VAMPzero.Component.Htp.Geometry.cHT import cHT
from VAMPzero.Component.Htp.Geometry.lHT import lHT
from VAMPzero.Component.Htp.Geometry.location import location
from VAMPzero.Component.Htp.Geometry.phi25 import phi25
from VAMPzero.Component.Htp.Geometry.phi50 import phi50
from VAMPzero.Component.Htp.Geometry.refArea import refArea
from VAMPzero.Component.Htp.Geometry.refAreaTakeOff import refAreaTakeOff 
from VAMPzero.Component.Htp.Geometry.refAreaCruise import refAreaCruise  
from VAMPzero.Component.Htp.Geometry.refAreaLanding import refAreaLanding
from VAMPzero.Component.Htp.Geometry.span import span
from VAMPzero.Component.Htp.Geometry.taperRatio import taperRatio
from VAMPzero.Component.Htp.Geometry.xMAC import xMAC
from VAMPzero.Component.Htp.Geometry.xRoot import xRoot
from VAMPzero.Component.Htp.Geometry.zRoot import zRoot
from VAMPzero.Component.Htp.Mass.mHtp import mHtp
from VAMPzero.Component.Main.Parameter.uID import uID
from VAMPzero.Component.Wing.Aerodynamic.cD0c import cD0c
from VAMPzero.Component.Wing.Aerodynamic.cLMAX import cLMAX
from VAMPzero.Component.Wing.Aerodynamic.cLalpha import cLalpha
from VAMPzero.Component.Wing.Aerodynamic.cfLAM import cfLAM
from VAMPzero.Component.Wing.Aerodynamic.cfTURB import cfTURB
from VAMPzero.Component.Wing.Aerodynamic.formFactor import formFactor
from VAMPzero.Component.Wing.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Wing.Geometry.cMAC import cMAC
from VAMPzero.Component.Htp.Geometry.cRoot import cRoot
from VAMPzero.Component.Wing.Geometry.cTip import cTip
from VAMPzero.Component.Wing.Geometry.dihedral import dihedral
from VAMPzero.Component.Htp.Geometry.expArea import expArea
from VAMPzero.Component.Wing.Geometry.phiLE import phiLE
from VAMPzero.Component.Wing.Geometry.phiTE import phiTE
from VAMPzero.Component.Wing.Geometry.tcAVG import tcAVG
from VAMPzero.Component.Wing.Geometry.wetArea import wetArea
from VAMPzero.Component.Wing.Geometry.yMAC import yMAC
from VAMPzero.Component.Wing.Geometry.xMAC25 import xMAC25
from VAMPzero.Component.Wing.wing import wing
from VAMPzero.Handler.Component import component
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.Export.HTP.htp import createHTP
from VAMPzero.Component.Wing.Aerodynamic.nLam import nLam
from VAMPzero.Component.Htp.Elevator.elevator import elevator


class htp(wing):
    '''
    The horizontal tailplane it inherits the wing class
    
    Several parameters are inherited from the wing as well!!!
    '''

    def __init__(self, aircraft):
        '''
        will initialize instance mainly used for documentation
        links to the aircraft instance
        initiates the airfoil class
        '''
        component.__init__(self)
        self.id = 'htp'
        self.aircraft = aircraft
        self.level = 2

        self.UID = uID(cpacsPath='/cpacs/toolspecific/vampZero/htpUID')

        # Mass
        self.mHtp = mHtp(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[2]/massDescription['+self.id+'_mass]/mass')
        self.parentUID = parameter(value=self.id, 
			cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[2]/massDescription['+self.id+'_mass]/parentUID')

        # CoG
        self.posCoG = posCoG(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[2]/massDescription['+self.id+'_mass]/location/x')

        # Geometry
        self.refArea = refArea()
        self.refAreaTakeOff = refAreaTakeOff() 
        self.refAreaCruise = refAreaCruise() 
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
        self.xMAC25 = xMAC25()
        self.phiLE = phiLE()
        self.phiTE = phiTE()
        self.phi25 = phi25()
        self.phi50 = phi50()
        self.xRoot = xRoot()
        self.zRoot = zRoot()
        self.lHT = lHT()
        self.cHT = cHT()
        self.dihedral = dihedral()
        self.LoD = LoD()
        self.location = location()


        # Aerodynamic
        self.cLalpha = cLalpha()
        self.cLMAX = cLMAX()
        #self.cLMIN = cLMIN()
        self.cLMAXht = cLMAXht()
        self.CLalphaHTP_TO = CLalphaHTP_TO()
        self.CLalphaHTP_CR = CLalphaHTP_CR()
        self.CLalphaHTP_L = CLalphaHTP_L()
        self.formFactor = formFactor()
        self.reynoldsNr = reynoldsNr()
        self.cfLAM = cfLAM()
        self.cfTURB = cfTURB()
        self.cD0c = cD0c()
        self.nLam = nLam()
        self.detadalpha = detadalpha()
        self.DPR = DPR()

        # Airfoil
        self.airfoilr = airfoil(self)  # Root Airfoil
        self.airfoilt = airfoil(self)  # Tip  Airfoil

        # Elevator
        self.elevator = elevator(self)
        

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        cpacsPath must be filled
        
        :Author: Jonas Jepsen
        :param CPACSObj: the CPACS object holding the data for export
        '''
        # self.LoD.setValue(1)    # level of detail [0,1]
        if self.location.getValue():
            xRoot = self.xRoot.getValue()
            zRoot = self.zRoot.getValue()
        else:
            vtp_span = self.aircraft.vtp.span.getValue()
            vtp_phiLE = (self.aircraft.vtp.phiLE.getValue())*pi/180.

            xRoot = tan(vtp_phiLE)*vtp_span
            try:
                xRoot = xRoot.real
            except:
                pass

            zRoot = vtp_span


        createHTP(CPACSObj, self.id, xRoot, zRoot, self.airfoilr.tc.getValue(), self.airfoilt.tc.getValue(), self.cRoot.getValue(),
                  self.cTip.getValue(), self.span.getValue(), self.phiLE.getValue(), self.dihedral.getValue(),
                  self.LoD.getValue(), self.location.getValue())

        super(wing, self).cpacsExport(CPACSObj)
        # self.exporter(CPACSObj)

###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
