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
from VAMPzero.Component.Wing.Aileron.aileron import aileron
from VAMPzero.Component.Wing.Geometry.location import location
from VAMPzero.Component.Wing.Slat.slat import slat
from VAMPzero.Component.Wing.Flap.flap import flap
from VAMPzero.Component.Wing.Spoiler.spoiler import spoiler
from VAMPzero.Component.Wing.Aerodynamic.cD0c import cD0c
from VAMPzero.Component.Wing.Aerodynamic.cDMINoffset import cDMINoffset
from VAMPzero.Component.Wing.Aerodynamic.cDw import cDw
from VAMPzero.Component.Wing.Aerodynamic.cLMAX import cLMAX
from VAMPzero.Component.Wing.Aerodynamic.cLalpha import cLalpha
from VAMPzero.Component.Wing.Aerodynamic.cfLAM import cfLAM
from VAMPzero.Component.Wing.Aerodynamic.cfTURB import cfTURB
from VAMPzero.Component.Wing.Aerodynamic.cM0CR import cM0CR
from VAMPzero.Component.Wing.Aerodynamic.formFactor import formFactor
from VAMPzero.Component.Wing.Aerodynamic.machCrit import machCrit
from VAMPzero.Component.Wing.Aerodynamic.machDD import machDD
from VAMPzero.Component.Wing.Aerodynamic.nLam import nLam
from VAMPzero.Component.Wing.Aerodynamic.oswald import oswald
from VAMPzero.Component.Wing.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Wing.CPACS.cFuselage import cFuselage
from VAMPzero.Component.Wing.CPACS.cKink import cKink
from VAMPzero.Component.Wing.CPACS.xFuselage import xFuselage
from VAMPzero.Component.Wing.CPACS.xKink import xKink
from VAMPzero.Component.Wing.CPACS.xTip import xTip
from VAMPzero.Component.Wing.CPACS.yFuselage import yFuselage
from VAMPzero.Component.Wing.CPACS.yKink import yKink
from VAMPzero.Component.Wing.CPACS.zFuselage import zFuselage
from VAMPzero.Component.Wing.CPACS.zKink import zKink
from VAMPzero.Component.Wing.CPACS.zTip import zTip
from VAMPzero.Component.Wing.CoG.posCoG import posCoG
from VAMPzero.Component.Wing.Geometry.LoD import LoD
from VAMPzero.Component.Wing.Geometry.aspectRatio import aspectRatio
from VAMPzero.Component.Wing.Geometry.cMAC import cMAC
from VAMPzero.Component.Wing.Geometry.cRoot import cRoot
from VAMPzero.Component.Wing.Geometry.cTip import cTip
from VAMPzero.Component.Wing.Geometry.dihedral import dihedral
from VAMPzero.Component.Wing.Geometry.etaKink import etaKink
from VAMPzero.Component.Wing.Geometry.expArea import expArea
from VAMPzero.Component.Wing.Geometry.phi25 import phi25
from VAMPzero.Component.Wing.Geometry.phi50 import phi50
from VAMPzero.Component.Wing.Geometry.phiLE import phiLE
from VAMPzero.Component.Wing.Geometry.phiTE import phiTE
from VAMPzero.Component.Wing.Geometry.refArea import refArea
from VAMPzero.Component.Wing.Geometry.span import span
from VAMPzero.Component.Wing.Geometry.taperRatio import taperRatio
from VAMPzero.Component.Wing.Geometry.tcAVG import tcAVG
from VAMPzero.Component.Wing.Geometry.twist import twist
from VAMPzero.Component.Wing.Geometry.wetArea import wetArea
from VAMPzero.Component.Wing.Geometry.xMAC import xMAC
from VAMPzero.Component.Wing.Geometry.xMAC25 import xMAC25
from VAMPzero.Component.Wing.Geometry.xRoot import xRoot
from VAMPzero.Component.Wing.Geometry.yMAC import yMAC
from VAMPzero.Component.Wing.Geometry.zRoot import zRoot
from VAMPzero.Component.Wing.Mass.mWing import mWing
from VAMPzero.Handler.Component import component
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.Export.Wing.Shape.functions import createWingAirfoil
from VAMPzero.Lib.CPACS.Export.Wing.wing import createWing
from VAMPzero.Component.Wing.Geometry.etaEngine import etaEngine
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD
from VAMPzero.Component.Wing.Aerodynamic.cM0TO import cM0TO
from VAMPzero.Component.Wing.Aerodynamic.cM0L import cM0L


class wing(component):
    '''
    class for the description of the wing
    inherits component for throwing errors
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
        self.id = 'wing'
        self.aircraft = aircraft
        self.level = 2
        self.UID = uID(cpacsPath='/cpacs/toolspecific/vampZero/wingUID')


        # Mass
        self.mWing = mWing(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[1]/massDescription['+self.id+'_mass]/mass')
        self.parentUID = parameter(value=self.id, 
			cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[1]/massDescription['+self.id+'_mass]/parentUID')

        # CoG
        self.posCoG = posCoG(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[1]/massDescription['+self.id+'_mass]/location/x')

        # Geometry
        self.location = location()		
        self.refArea = refArea(cpacsPath='/cpacs/vehicles/aircraft/model/reference/area')
        self.expArea = expArea()
        self.wetArea = wetArea()
        self.aspectRatio = aspectRatio()
        self.span = span()
        self.taperRatio = taperRatio()
        self.tcAVG = tcAVG()
        self.cRoot = cRoot()
        self.cTip = cTip()
        self.cMAC = cMAC(cpacsPath='/cpacs/vehicles/aircraft/model/reference/length')
        self.yMAC = yMAC()
        self.xMAC = xMAC()
        self.xMAC25 = xMAC25(cpacsPath='/cpacs/vehicles/aircraft/model/reference/point/x')
        self.phiLE = phiLE()
        self.phiTE = phiTE()
        self.phi25 = phi25()
        self.phi50 = phi50()
        self.dihedral = dihedral()
        self.twist = twist()
        self.xRoot = xRoot()
        self.zRoot = zRoot()
        self.LoD = LoD()
        self.etaKink = etaKink()
        self.etaEngine = etaEngine()

        # Aerodynamics
        self.cLalpha = cLalpha()
        self.cLMAX = cLMAX()
        self.formFactor = formFactor()
        self.reynoldsNr = reynoldsNr()  # cpacsPath='/cpacs/vehicles/aircraft/model/global/aeroPerformanceMap/reynoldsNumber')
        self.cfLAM = cfLAM()
        self.cfTURB = cfTURB()
        self.cD0c = cD0c()
        self.oswald = oswald()
        self.cDMINoffset = cDMINoffset()
        self.nLam = nLam()
        self.cDw = cDw()
        self.machDD = machDD()
        self.machCrit = machCrit()
        self.cM0CR = cM0CR()
        self.cM0TO = cM0TO()
        self.cM0L = cM0L()


        # Airfoil
        self.airfoilr = airfoil(self, position='root')
        self.airfoilt = airfoil(self, position='tip')

        # Aileron
        self.aileron = aileron(self)

        # Slat
        self.slat = slat(self)

        # Flap
        self.flap = flap(self)

        # Spoiler
        self.spoiler = spoiler(self)

        # CPACS Stuff for Export to higher Level
        self.xFuselage = xFuselage()
        self.yFuselage = yFuselage()
        self.zFuselage = zFuselage()
        self.cFuselage = cFuselage()

        self.xKink = xKink()
        self.yKink = yKink()
        self.zKink = zKink()
        self.cKink = cKink()

        self.xTip = xTip()
        self.zTip = zTip()

    ###################################################################################################
    # #Export to CPACS
    ###################################################################################################

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well.
        cpacsPath must be filled
        @author: Jonas Jepsen
        @param CPACSObj: the CPACS object holding the data for export
        '''
        if self.aircraft.strut.active.getValue():
            self.LoD.setValueFix(WING_LOD.SBW)

        try:
            etaKink = self.etaKink.getValue() 
            etaEngine = self.aircraft.engine.yEngine.getValue() / self.span.getValue() * 2. 
            createWingAirfoil(CPACSObj)
            createWing(CPACSObj, id=self.id, zeroWing=self, LoD=self.LoD.getValue())        
        except ZeroDivisionError, e:
            self.log.warning('VAMPzero EXPORT: WING could not be created due to "%s"!', e)
        super(wing, self).cpacsExport(CPACSObj)

        ####################################################################################################
        # #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ####################################################################################################
