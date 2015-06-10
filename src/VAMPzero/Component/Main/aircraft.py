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

from VAMPzero.Component.Atmosphere.atmosphere import atmosphere
from VAMPzero.Component.Engine.engine import engine
from VAMPzero.Component.Fuel.fuel import fuel
from VAMPzero.Component.Fuselage.fuselage import fuselage
from VAMPzero.Component.Htp.htp import htp
from VAMPzero.Component.LandingGear.landingGear import landingGear
from VAMPzero.Component.Main.Aerodynamic.cD0 import cD0
from VAMPzero.Component.Main.Aerodynamic.cDCR import cDCR
from VAMPzero.Component.Main.Aerodynamic.cLCR import cLCR
from VAMPzero.Component.Main.Aerodynamic.cLL import cLL
from VAMPzero.Component.Main.Aerodynamic.cDL import cDL
from VAMPzero.Component.Main.Aerodynamic.cLMAX import cLMAX
from VAMPzero.Component.Main.Aerodynamic.cLTO import cLTO
from VAMPzero.Component.Main.Aerodynamic.cDTO import cDTO
from VAMPzero.Component.Main.Aerodynamic.loDCLIMB import loDCLIMB
from VAMPzero.Component.Main.Aerodynamic.loDCR import loDCR
from VAMPzero.Component.Main.Aerodynamic.loDLOI import loDLOI
from VAMPzero.Component.Main.Aerodynamic.loDTO import loDTO
from VAMPzero.Component.Main.Aerodynamic.oswald import oswald
from VAMPzero.Component.Main.Aerodynamic.cLROLL import cLROLL
from VAMPzero.Component.Main.CoG.posCoG import posCoG
from VAMPzero.Component.Main.CoG.posNP import posNP
from VAMPzero.Component.Main.CoG.posCoGOEM import posCoGOEM
from VAMPzero.Component.Main.CoG.posCoGMIN import posCoGMIN
from VAMPzero.Component.Main.CoG.posCoGMAX import posCoGMAX
from VAMPzero.Component.Main.CoG.static_margin import static_margin
from VAMPzero.Component.Main.Crew.nCabinCrew import nCabinCrew
from VAMPzero.Component.Main.Crew.nPilot import nPilot
from VAMPzero.Component.Main.DOC.C1 import C1
from VAMPzero.Component.Main.DOC.C2 import C2
from VAMPzero.Component.Main.DOC.COC import COC
from VAMPzero.Component.Main.DOC.COO import COO
from VAMPzero.Component.Main.DOC.C1 import C1
from VAMPzero.Component.Main.DOC.C2 import C2
from VAMPzero.Component.Main.DOC.aFactor import aFactor
from VAMPzero.Component.Main.DOC.costCap import costCap
from VAMPzero.Component.Main.DOC.flightCycles import flightCycles
from VAMPzero.Component.Main.DOC.DOC import DOC
from VAMPzero.Component.Main.DOC.USDexchangeEURO import USDexchangeEURO
from VAMPzero.Component.Main.DOC.aFactor import aFactor
from VAMPzero.Component.Main.DOC.costCap import costCap
from VAMPzero.Component.Main.DOC.costCrew import costCrew
from VAMPzero.Component.Main.DOC.costDepreciation import costDepreciation
from VAMPzero.Component.Main.DOC.costFuel import costFuel
from VAMPzero.Component.Main.DOC.costGround import costGround
from VAMPzero.Component.Main.DOC.costInsurance import costInsurance
from VAMPzero.Component.Main.DOC.costInterest import costInterest
from VAMPzero.Component.Main.DOC.costLanding import costLanding
from VAMPzero.Component.Main.DOC.costMaintenance import costMaintenance
from VAMPzero.Component.Main.DOC.costNavigation import costNavigation
from VAMPzero.Component.Main.DOC.flightCycles import flightCycles
from VAMPzero.Component.Main.DOC.inflation import inflation
from VAMPzero.Component.Main.DOC.priceAircraft import priceAircraft
from VAMPzero.Component.Main.DOC.priceFuel import priceFuel
from VAMPzero.Component.Main.DOC.tBlock import tBlock
from VAMPzero.Component.Main.DOC.utilization import utilization
from VAMPzero.Component.Main.Inertia.massIX import massIX
from VAMPzero.Component.Main.Inertia.massIY import massIY
from VAMPzero.Component.Main.Inertia.massIZ import massIZ
from VAMPzero.Component.Main.Mass.mLM import mLM
from VAMPzero.Component.Main.Mass.mTOM import mTOM
from VAMPzero.Component.Main.Mass.mZFW import mZFW
from VAMPzero.Component.Main.Mass.oEM import oEM
from VAMPzero.Component.Main.Mass.oIM import oIM
from VAMPzero.Component.Main.Parameter.uID import uID
from VAMPzero.Component.Main.Performance.IASCLIMB import IASCLIMB
from VAMPzero.Component.Main.Performance.IASDESCENT import IASDESCENT
from VAMPzero.Component.Main.Performance.altCR import altCR
from VAMPzero.Component.Main.Performance.desRange import desRange
from VAMPzero.Component.Main.Performance.distCLIMB import distCLIMB
from VAMPzero.Component.Main.Performance.distCR import distCR
from VAMPzero.Component.Main.Performance.distDESCENT import distDESCENT
from VAMPzero.Component.Main.Performance.distRES import distRES
from VAMPzero.Component.Main.Performance.gammaCLIMB import gammaCLIMB
from VAMPzero.Component.Main.Performance.gammaDESCENT import gammaDESCENT
from VAMPzero.Component.Main.Performance.machCR import machCR
from VAMPzero.Component.Main.Performance.rangeType import rangeType
from VAMPzero.Component.Main.Performance.sLFL import sLFL
from VAMPzero.Component.Main.Performance.sTOFL import sTOFL
from VAMPzero.Component.Main.Performance.timeCLIMB import timeCLIMB
from VAMPzero.Component.Main.Performance.timeCR import timeCR
from VAMPzero.Component.Main.Performance.timeDESCENT import timeDESCENT
from VAMPzero.Component.Main.Performance.timeRES import timeRES
from VAMPzero.Component.Main.Sizing.twTO import twTO
from VAMPzero.Component.Main.Sizing.wsL import wsL
from VAMPzero.Component.Main.Sizing.wsMAX import wsMAX
from VAMPzero.Component.Main.Sizing.wsTO import wsTO
#from VAMPzero.Component.Main.Stability.staticMargin import staticMargin
#from VAMPzero.Component.Main.Controllability.refAreaHtpMIN import refAreaHtpMIN
from VAMPzero.Component.Payload.payload import payload
from VAMPzero.Component.Pylon.pylon import pylon
from VAMPzero.Component.Strut.strut import strut
from VAMPzero.Component.Systems.systems import systems
from VAMPzero.Component.Tool.tool import tool
from VAMPzero.Component.Vtp.vtp import vtp
from VAMPzero.Component.Wing.wing import wing
from VAMPzero.Handler.Component import component
from VAMPzero.Component.Main.DOC.costEmissionTrade import costEmissionTrade
from VAMPzero.Component.Main.DOC.tFlight import tFlight
from VAMPzero.Component.Main.DOC.costEngineMaintenance import costEngineMaintenance
from VAMPzero.Component.Main.DOC.costAircraftMaintenance import costAircraftMaintenance
from VAMPzero.Component.Main.Sizing.twFAR25121a import twFAR25121a
from VAMPzero.Component.Main.Sizing.twFAR25121b import twFAR25121b
from VAMPzero.Component.Main.Sizing.twTOP25 import twTOP25
from VAMPzero.Component.Main.Performance.sTOFLISA import sTOFLISA
from VAMPzero.Handler.Parameter import parameter



class aircraft(component):
    ''' 
    The global aircraft class holds parameters and components adjacent to the aircraft. 
    It inherits the component class to access exceptions and stuff.
    '''

    def __init__(self):
        '''
        will initialize all values upon creation of the instance. Mainly used for documentation
        '''
        component.__init__(self)
        self.id = 'aircraft'
        self.level = 1

        self.modelUID = uID(cpacsPath='/cpacs/toolspecific/vampZero/aircraftModelUID')
        self.version  = parameter(value=0.1, cpacsPath='/cpacs/header/version')

        #Mass Data
        self.mLM = mLM(cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mMLM/mass')
        self.mTOM = mTOM(cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mTOM/mass')
        self.mZFW = mZFW(cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mZFM/mass')
        self.oEM = oEM(cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/massDescription/mass')
        self.oIM = oIM(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mOperatorItems/massDescription/mass')

        #CoG
        self.posCoG = posCoG(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mTOM/location/x')
        self.posNP = posNP()
        self.posCoGOEM = posCoGOEM()
        self.posCoGMIN = posCoGMIN()
        self.posCoGMAX = posCoGMAX()
        self.static_margin = static_margin()

        #Inertia
        self.massIX = massIX(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mTOM/massInertia/Jxx')
        self.massIY = massIY(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mTOM/massInertia/Jyy')
        self.massIZ = massIZ(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/designMasses/mTOM/massInertia/Jzz')

        #Performance Data       
        self.desRange = desRange() #@todo: set correct xpath (cpacsPath='/cpacs/vehicles/aircraft/model/global/designRange')
        self.machCR = machCR(cpacsPath='/cpacs/vehicles/aircraft/model/global/machCruise')
        self.altCR = altCR()
        self.sTOFL = sTOFL()
        self.sTOFLISA = sTOFLISA()
        self.sLFL = sLFL() #@todo: set correct xpath (cpacsPath='/cpacs/vehicles/aircraft/model/global/sFL')
        self.rangeType = rangeType()
        self.timeRES = timeRES()
        self.timeDESCENT = timeDESCENT()
        self.timeCLIMB = timeCLIMB()
        self.timeCR = timeCR()
        self.distRES = distRES()
        self.distDESCENT = distDESCENT()
        self.distCLIMB = distCLIMB()
        self.distCR = distCR()
        self.gammaCLIMB = gammaCLIMB()
        self.gammaDESCENT = gammaDESCENT()
        self.IASCLIMB = IASCLIMB()
        self.IASDESCENT = IASDESCENT()

        #Crew Data
        self.nPilot = nPilot()
        self.nCabinCrew = nCabinCrew()

        #Sizing Data
        self.wsTO = wsTO()
        self.wsL = wsL()
        self.wsMAX = wsMAX()
        self.twTO = twTO()
        self.twFAR20121a = twFAR25121a()
        self.twFAR20121b = twFAR25121b()
        self.twTOP25 = twTOP25()

        #Aerodynamics Data
        self.cLCR = cLCR()
        self.cLMAX = cLMAX()
        self.cLTO = cLTO()
        self.cLL = cLL()
        self.cDCR = cDCR()
        self.cDTO = cDTO()
        self.cDL = cDL()
        self.cD0 = cD0()
        self.loDCR = loDCR()
        self.loDTO = loDTO()
        self.loDLOI = loDLOI()
        self.loDCLIMB = loDCLIMB()
        self.oswald = oswald()
        self.cLROLL = cLROLL()

        #DOC
        self.aFactor = aFactor()
        self.inflation = inflation()
        self.USDexchangeEURO = USDexchangeEURO()
        self.tBlock = tBlock()
        self.tFlight = tFlight()
        self.utilization = utilization()
        self.costDepreciation = costDepreciation()
        self.costFuel = costFuel()
        self.costMaintenance = costMaintenance()
        self.costAircraftMaintenance = costAircraftMaintenance()
        self.costEngineMaintenance = costEngineMaintenance()
        self.costCrew = costCrew()
        self.costCap = costCap()
        self.costGround = costGround()
        self.costNavigation = costNavigation()
        self.costLanding = costLanding()
        self.costInterest = costInterest()
        self.costInsurance = costInsurance()
        self.costEmissionTrade = costEmissionTrade()
        self.flightCycles = flightCycles()
        self.priceFuel = priceFuel()
        self.priceAircraft = priceAircraft()
        self.DOC = DOC()
        self.COC = COC()
        self.COO = COO()
        self.C1 = C1()
        self.C2 = C2()
        self.aFactor = aFactor()
        self.costCap = costCap()
        self.flightCycles = flightCycles()

        #Stability
        #self.staticMargin = staticMargin()
        
        #Controllability
        #self.refAreaHtpMIN = refAreaHtpMIN()

        #Component Objects
        self.wing = wing(self)
        self.strut = strut(self)
        self.fuselage = fuselage(self)
        self.vtp = vtp(self)
        self.htp = htp(self)
        self.engine = engine(self)
        self.landingGear = landingGear(self)
        self.systems = systems(self)
        self.payload = payload(self)
        self.pylon = pylon(self)
        self.fuel = fuel(self)
        self.atmosphere = atmosphere(self)
        self.tool = tool(self)
