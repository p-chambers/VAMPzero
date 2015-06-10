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
from VAMPzero.Component.Engine.Aerodynamic.cD0c import cD0c
from VAMPzero.Component.Engine.Aerodynamic.cfLAM import cfLAM
from VAMPzero.Component.Engine.Aerodynamic.cfTURB import cfTURB
from VAMPzero.Component.Engine.Aerodynamic.formFactor import formFactor
from VAMPzero.Component.Engine.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Engine.CoG.posCoG import posCoG
from VAMPzero.Component.Engine.Geometry.dEngine import dEngine
from VAMPzero.Component.Engine.Geometry.lEngine import lEngine
from VAMPzero.Component.Engine.Geometry.location import location
from VAMPzero.Component.Engine.Geometry.wetArea import wetArea
from VAMPzero.Component.Engine.Geometry.xEngine import xEngine
from VAMPzero.Component.Engine.Geometry.yEngine import yEngine
from VAMPzero.Component.Engine.Geometry.zEngine import zEngine
from VAMPzero.Component.Engine.Intertia.massIX import massIX
from VAMPzero.Component.Engine.Intertia.massIY import massIY
from VAMPzero.Component.Engine.Intertia.massIZ import massIZ
from VAMPzero.Component.Engine.Mass.mEngine import mEngine
from VAMPzero.Component.Engine.Propulsion.OPR import OPR
from VAMPzero.Component.Engine.Propulsion.TET import TET
from VAMPzero.Component.Engine.Propulsion.bypassRatio import bypassRatio
from VAMPzero.Component.Engine.Propulsion.etaCompr import etaCompr
from VAMPzero.Component.Engine.Propulsion.etaFan import etaFan
from VAMPzero.Component.Engine.Propulsion.etaProp import etaProp
from VAMPzero.Component.Engine.Propulsion.etaTherm import etaTherm
from VAMPzero.Component.Engine.Propulsion.etaTransm import etaTransm
from VAMPzero.Component.Engine.Propulsion.etaTurb import etaTurb
from VAMPzero.Component.Engine.Propulsion.mDotEngine import mDotEngine
from VAMPzero.Component.Engine.Propulsion.nEngine import nEngine
from VAMPzero.Component.Engine.Propulsion.sfcCR import sfcCR
from VAMPzero.Component.Engine.Propulsion.sfcLOI import sfcLOI
from VAMPzero.Component.Engine.Propulsion.thrustCR import thrustCR
from VAMPzero.Component.Engine.Propulsion.thrustTO import thrustTO
from VAMPzero.Component.Engine.Propulsion.thrustTWDat import thrustTWDat
from VAMPzero.Component.Main.Parameter.uID import uID
from VAMPzero.Handler.Component import component
from VAMPzero.Component.Engine.Aerodynamic.nLam import nLam
from VAMPzero.Component.Engine.Aerodynamic.dCDOEI import dCDOEI
from VAMPzero.Component.Engine.Propulsion.thrustTOISA import thrustTOISA


class engine(component):
    '''
    
    .. todo:: 
    
       component engine: think about implementing engines 
       as singulars and the allowing multiple objects within one aircraft
       
    .. todo:: 
    
       component engine: currently more a mix of nacelle and engine
        
    '''

    def __init__(self, aircraft):
        '''
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'engine'
        self.aircraft = aircraft
        self.level = 2
        self.UID = uID(cpacsPath='/cpacs/toolspecific/vampZero/engineUID')


        #Mass
        self.mEngine = mEngine(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mPowerUnits/massDescription/mass')

        #CoG
        self.posCoG = posCoG()

        #Inertia
        self.massIX = massIX(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mPowerUnits/massDescription/massInertia/Jxx')
        self.massIY = massIY(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mPowerUnits/massDescription/massInertia/Jyy')
        self.massIZ = massIZ(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mPowerUnits/massDescription/massInertia/Jzz')

        #Geometry
        self.lEngine = lEngine(cpacsPath='/cpacs/vehicles/engines/engine/geometry/length')
        self.dEngine = dEngine(cpacsPath='/cpacs/vehicles/engines/engine/geometry/diameter')
        self.yEngine = yEngine(cpacsPath='/cpacs/vehicles/aircraft/model/engines/engine/transformation/translation/y')
        self.xEngine = xEngine(cpacsPath='/cpacs/vehicles/aircraft/model/engines/engine/transformation/translation/x')
        self.zEngine = zEngine(cpacsPath='/cpacs/vehicles/aircraft/model/engines/engine/transformation/translation/z')
        self.wetArea = wetArea()
        self.location = location()

        #Aerodynamics
        self.formFactor = formFactor()
        self.reynoldsNr = reynoldsNr()
        self.cfLAM = cfLAM()
        self.cfTURB = cfTURB()
        self.cD0c = cD0c()
        self.dCDOEI = dCDOEI()
        self.nLam = nLam()

        #Propulsion
        self.mDotEngine = mDotEngine()
        self.thrustTO = thrustTO(cpacsPath='/cpacs/vehicles/engines/engine/analysis/thrust00')
        self.thrustTOISA = thrustTOISA()
        self.thrustCR = thrustCR()
        self.nEngine = nEngine()
        self.sfcCR = sfcCR()
        self.sfcLOI = sfcLOI()
        self.bypassRatio = bypassRatio(cpacsPath='/cpacs/vehicles/engines/engine/analysis/bpr00')
        self.thrustTWDat = thrustTWDat(cpacsPath='/cpacs/toolspecific/tWDat/thrust00Scaling')
        self.etaCompr = etaCompr()
        self.etaFan = etaFan()
        self.etaProp = etaProp()
        self.etaTherm = etaTherm()
        self.etaTransm = etaTransm()
        self.etaTurb = etaTurb()
        self.TET = TET()
        self.OPR = OPR()

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################