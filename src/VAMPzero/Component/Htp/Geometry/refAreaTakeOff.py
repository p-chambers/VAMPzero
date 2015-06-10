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
from cmath import sqrt, pi, cos, tan, atan
import numpy as np
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSurfaceArea

import time
class refAreaTakeOff(parameter):
    '''
    The reference area of the horizontal tailplane for the Take Off.
    
    :Unit: [m2]

    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refAreaTakeOff, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)


    def calc(self):
        '''
        Calculates the reference area for the HTP from the maximum value of the different calculations.
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        refAreaStability = self.calcStability()
        refAreaRotationStatic = self.calcRotationStatic()
        refAreaControl = self.calcControl()

        refAreaStability = refAreaStability.real            #in any case of complex values (with +- 0j) guarantee for real values
        refAreaRotationStatic = refAreaRotationStatic.real
        refAreaControl = refAreaControl.real
        
        #Calculates the maximum of the previous area computations
        refAreaTakeOff = max(refAreaStability,refAreaRotationStatic,refAreaControl)
        
        return self.setValueCalc(refAreaTakeOff) 
    
    def calcStability(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the climb phase.
        It is calculated the area of the HTP, for which the aircraft is natural stable in case of the maximum aft posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        mTOM = self.parent.aircraft.mTOM.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        cLTO = self.parent.aircraft.cLTO.getValue()
        refArea = self.parent.aircraft.wing.refArea.getValue()
        aspectRatioWing = self.parent.aircraft.wing.aspectRatio.getValue()
        phi50Wing = self.parent.aircraft.wing.phi50.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        aAP = self.parent.aircraft.atmosphere.aAP.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        static_margin = self.parent.aircraft.static_margin.getValue()
        CLalphaHTP = self.parent.CLalphaHTP_TO.getValue()
        DPR = self.parent.DPR.getValue()
        dalphaW_dalpha = self.parent.detadalpha.getValue()

        g = 9.81
        vs = sqrt(2 * mTOM * g / (rhoAP * cLTO * refArea))
        v2 = 1.2 * vs

        machTO = v2/aAP 
        qR = rhoAP/2 * v2**2
        qHTP_TO = DPR * qR

        CLalphaWing = (2 * pi * aspectRatioWing)/(2 + (aspectRatioWing**2 * (tan(phi50Wing*pi/180)**2 + 1 - machTO**2) + 4)**0.5)

        posCoGMAX = self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay
        refAreaStability_var = wingrefArea * (qR/qHTP_TO) * (CLalphaWing*(posCoGMAX - wingxMAC25
                                  - static_margin*wingcMAC)) / (CLalphaHTP*(1 - dalphaW_dalpha)*(lHT - posCoGMAX
                                  + wingxMAC25 + static_margin*wingcMAC))

        refAreaStability = refAreaStability_var.max()
        
        if refAreaStability < 0:
            refAreaStability = 1.

        return refAreaStability

    def calcRotationStatic(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the rotation phase of the aircraft.
        It is calculated the area of the HTP, for which there is enough control area to rotate the aircraft in case of the minimum fwd posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        cLMAXht = self.parent.cLMAXht.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcM0TO = self.parent.aircraft.wing.cM0TO.getValue()
        xLG = self.parent.aircraft.landingGear.xLandingGear.getValue()
        zLG = self.parent.aircraft.landingGear.zLandingGear.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()
        oswald = self.parent.aircraft.wing.oswald.getValue()
        lHT = self.parent.lHT.getValue()
        cD0 = self.parent.aircraft.cD0.getValue()
        dCDTO = self.parent.aircraft.wing.flap.dCDTO.getValue()        
        dCDextendedLG = self.parent.aircraft.landingGear.dCDextendedLG.getValue()
        CLRollTO = self.parent.aircraft.cLROLL.getValue()
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        cLTO = self.parent.aircraft.cLTO.getValue()
        refArea = self.parent.aircraft.wing.refArea.getValue()
        DPR = self.parent.DPR.getValue()
        x1 = self.parent.aircraft.sTOFL.x1
        zEngine = -(self.parent.aircraft.engine.zEngine.getValue()) #zEngine is defined in VAMPzero as a negative value, but for the following equilibrium of
                                                                    #the moments, a positive value of zEngine is needed for engines, which are installed
                                                                    #below the wing (default configuration)

        g = 9.81
        vs = sqrt(2 * mTOM * g / (rhoAP * cLTO * refArea))
        v1 = vs
        v2 = 1.2 * vs

        qR = rhoAP/2 * v2**2
        qHTP_TO = DPR * qR

        mu = 0.025                #Coefficient of friction between beton/asphalt and gum
        kR = 1.2
        
        posCoGMIN = self.parent.aircraft.posCoGMAX.posCoGMIN_fuel_pay
        cLTO_var = (2 * self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81)/(rhoAP * v1**2 * wingrefArea)
        cDTO_var = cD0 + dCDTO + dCDextendedLG + cLTO_var**2/(pi * aspectRatio * oswald)
        #Assumption: Thrust equals roll drag, aerodynamic drag and acceleration to v1 in x1 
        thrust_TO_var = (mu * self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81 + rhoAP/2 * v1**2 * cDTO_var * wingrefArea + self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * v1**2/(2* x1))/ nEngine
        if zEngine > 0:     #The critical case for the htp, when the engines are installed below the wing (below the CoG), is without consideration of the thrust 
            thrustTO = thrust_TO_var * 0
        else:               #Engines above the wing (above the CoG), the moment of the thrust works against the rotation, the HTP has to be bigger
            thrustTO = thrust_TO_var 
        refAreaRotationStatic_var = ((cLTO_var * qR)/(cLMAXht * qHTP_TO))/(lHT - posCoGMIN + wingxMAC25 - (xLG - posCoGMIN
                                        + mu* zLG)*(1 - 1/kR**2)) * ((xLG - posCoGMIN + mu * zLG)/kR**2 
                                        - (wingcMAC * wingcM0TO)/cLTO_var - (nEngine * thrustTO * zEngine)/(cLTO_var * qR * wingrefArea)
                                        - (xLG - wingxMAC25 + mu* zLG)*(CLRollTO/cLTO_var)) * wingrefArea

        refAreaRotationStatic = refAreaRotationStatic_var.max()

        return refAreaRotationStatic 
        
    def calcControl(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the climb phase.
        It is calculated the area of the HTP, so that the aircraft can be stabilized in case of the minimum fwd posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        cLMAXht = self.parent.cLMAXht.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingcM0TO = self.parent.aircraft.wing.cM0TO.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()
        oswald = self.parent.aircraft.wing.oswald.getValue()
        cD0 = self.parent.aircraft.cD0.getValue()
        dCDTO = self.parent.aircraft.wing.flap.dCDTO.getValue()        
        dCDextendedLG = self.parent.aircraft.landingGear.dCDextendedLG.getValue()
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        cLTO = self.parent.aircraft.cLTO.getValue()
        refArea = self.parent.aircraft.wing.refArea.getValue()
        DPR = self.parent.DPR.getValue()
        zEngine = -(self.parent.aircraft.engine.zEngine.getValue())   #zEngine is defined in VAMPzero as a negative value, but for the following equilibrium of 
                                                                      #the moments, a positive value of zEngine is needed for engines, which are installed
                                                                      #below the wing 
        g = 9.81
        vs = sqrt(2 * mTOM * g / (rhoAP * cLTO * refArea))
        v2 = 1.2 * vs

        x1 = self.parent.aircraft.sTOFL.x1

        qR = rhoAP/2 * v2**2
        qHTP_TO = DPR * qR

        mu = 0.025
        cLMAXht = -cLMAXht

        posCoGMIN = self.parent.aircraft.posCoGMAX.posCoGMIN_fuel_pay
        posCoGMAX = self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay
        cLTO_var = (2 * self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81)/(rhoAP * v2**2 * wingrefArea)
        cDTO_var = cD0 + dCDTO + dCDextendedLG + cLTO_var**2/(pi * aspectRatio * oswald)
        #Assumption: Thrust equals roll drag, aerodynamic drag and acceleration to v2 in x1
        thrust_TO_var = (mu * self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81 + rhoAP/2 * v2**2 * cDTO_var * wingrefArea + self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * v2**2/(2* x1))/ nEngine
        if zEngine > 0:     #The critical case for the htp, when the engines are installed below the wing (below the CoG), is without consideration of the thrust
            thrustTO = thrust_TO_var * 0
        else:               #Engines above the wing (above the CoG), the moment of the thrust works against the rotation, the HTP has to be bigger
            thrustTO = thrust_TO_var
        refAreaControl_var_min = (qR)/(qHTP_TO * cLMAXht * lHT) * ((self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81)/(qR * wingrefArea)
                                    * (posCoGMIN - wingxMAC25) + wingcM0TO * wingcMAC
                                    + (thrustTO * nEngine * zEngine)/(qR * wingrefArea)) * wingrefArea
        refAreaControl_var_max = (qR)/(qHTP_TO * cLMAXht * lHT) * ((self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81)/(qR * wingrefArea)
                                    * (posCoGMAX - wingxMAC25) + wingcM0TO * wingcMAC
                                    + (thrustTO * nEngine * zEngine)/(qR * wingrefArea)) * wingrefArea

        refAreaControl_min = refAreaControl_var_min.max()
        refAreaControl_max = refAreaControl_var_max.min()
        refAreaControl = max(refAreaControl_min,refAreaControl_max)

        return refAreaControl