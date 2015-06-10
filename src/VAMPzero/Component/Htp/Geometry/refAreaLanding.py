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


class refAreaLanding(parameter):
    '''
    The reference area of the horizontal tailplane
    
    :Unit: [m2]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refAreaLanding, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reference area for the HTP from the maximum value of the different calculations.
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        refAreaStability = self.calcStability()
        refAreaControl = self.calcControl()
        refAreaGoAround = self.calcGoAround()

        refAreaStability = refAreaStability.real            #in any case of complex values (with +- 0j) guarantee for real values
        refAreaControl = refAreaControl.real
        refAreaGoAround = refAreaGoAround.real
        
        #Calculates the maximum of the previous area computations        
        refAreaLanding = max(refAreaStability, refAreaControl, refAreaGoAround)
        
        return self.setValueCalc(refAreaLanding)
        
    def calcStability(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the landing phase.
        It is calculated the area of the HTP, for which the aircraft is natural stable in case of the maximum aft posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        aAP = self.parent.aircraft.atmosphere.aAP.getValue()
        aspectRatioWing = self.parent.aircraft.wing.aspectRatio.getValue() 
        phi50Wing = self.parent.aircraft.wing.phi50.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        static_margin = self.parent.aircraft.static_margin.getValue()
        CLalphaHTP = self.parent.CLalphaHTP_TO.getValue()
        wsL = self.parent.aircraft.wsL.getValue()
        cLL = self.parent.aircraft.cLL.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        DPR = self.parent.DPR.getValue()
        dalphaW_dalpha = self.parent.detadalpha.getValue()

        #Stall speed Calculation
        vL = sqrt(2 * wsL * 9.81 / (rhoAP * cLL))*1.2 #Eq. 3.1 from Roskam I p-90

        machL = vL/aAP
        qL = rhoAP/2 * vL**2
        qHTP_L = DPR * qL
        
        CLalphaWing = (2 * pi * aspectRatioWing)/(2 + (aspectRatioWing**2 * (tan(phi50Wing*pi/180)**2 + 1 - machL**2) + 4)**0.5)
        CLalphaWing = CLalphaWing.real

        posCoGMAX = self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay
        refAreaStability_var = wingrefArea * (qL/qHTP_L) * (CLalphaWing*(posCoGMAX - wingxMAC25 
                                  - static_margin*wingcMAC)) / (CLalphaHTP*(1 - dalphaW_dalpha)*(lHT - posCoGMAX
                                  + wingxMAC25 + static_margin*wingcMAC))

        refAreaStability = refAreaStability_var.max()
        
        if refAreaStability < 0:
            refAreaStability = 1.
        return refAreaStability
        
    def calcControl(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the landing phase.
        It is calculated the area of the HTP, so that the aircraft can be stabilized in case of the minimum fwd posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        mLM = self.parent.aircraft.mLM.getValue()
        cLMAXht = self.parent.cLMAXht.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingcM0L = self.parent.aircraft.wing.cM0L.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()
        oswald = self.parent.aircraft.wing.oswald.getValue()
        cD0 = self.parent.aircraft.cD0.getValue()
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        DPR = self.parent.DPR.getValue()
        zEngine = -(self.parent.aircraft.engine.zEngine.getValue())   #zEngine is defined in VAMPzero as a negative value, but for the following equilibrium of 
                                                                      #the moments, a positive value of zEngine is needed for engines, which are installed
                                                                      #below the wing 
        wsL = self.parent.aircraft.wsL.getValue()
        cLL = self.parent.aircraft.cLL.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()

        #Stall speed Calculation
        vL = sqrt(2 * wsL * 9.81 / (rhoAP * cLL))*1.2 #Eq. 3.1 from Roskam I p-90

        qL = rhoAP/2 * vL**2
        qHTP_L = DPR * qL

        cLMAXht = -cLMAXht

        # The current Landing Mass has to be smaller than the permitted landing mass
        # To enable vector operations we run the if statement on array level and then delete the according elements
        elementsNotToConsider = np.where(self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay[self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay>mLM])
        posCoGMIN = np.delete(self.parent.aircraft.posCoGMAX.posCoGMIN_fuel_pay, elementsNotToConsider)
        posCoGMAX = np.delete(self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay, elementsNotToConsider)
        m_TOW_fuel_pay = np.delete(self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay, elementsNotToConsider)

        cLL_var = (2 * m_TOW_fuel_pay * 9.81)/(rhoAP * vL**2 * wingrefArea)
        cDL_var = cD0 + cLL_var**2/(pi * aspectRatio * oswald)
        thrust_L_var = rhoAP/2 * vL**2 * cDL_var * wingrefArea
        if zEngine > 0:     #The critical case for the htp, when the engines are installed below the wing (below the CoG), is without consideration of the thrust
            thrustL = thrust_L_var * 0
        else:               #Engines above the wing (above the CoG), the moment of the thrust works against the rotation, the HTP has to be bigger
            thrustL = thrust_L_var
        refAreaControl_var_min = (qL)/(qHTP_L * cLMAXht * lHT) * ((m_TOW_fuel_pay * 9.81)/(qL * wingrefArea)
                                    * (posCoGMIN - wingxMAC25) + wingcM0L * wingcMAC
                                    + (thrustL * nEngine * zEngine)/(qL * wingrefArea)) * wingrefArea
        refAreaControl_var_max = (qL)/(qHTP_L * cLMAXht * lHT) * ((m_TOW_fuel_pay * 9.81)/(qL * wingrefArea)
                                    * (posCoGMAX - wingxMAC25) + wingcM0L * wingcMAC
                                    + (thrustL * nEngine * zEngine)/(qL * wingrefArea)) * wingrefArea

        refAreaControl_min = refAreaControl_var_min.max()
        refAreaControl_max = refAreaControl_var_max.min()
        refAreaControl = max(refAreaControl_min,refAreaControl_max)

        return refAreaControl
        
    def calcGoAround(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the landing phase.
        It is calculated the area of the HTP in case of full thrust, so that the aircraft can be stabilized in case of the minimum fwd posCoG.
        For aircraft with the engines installed below the wing, the area of the HTP has to be calculated for the maximum aft posCoG, because then
        there is less moment by the aircraft mass, which acts against the full thrust and the lift of the HPT has to be greater.
        For aircraft with the engines installed above the wing, the area of the HTP has to be calculated for the minimum fwd posCoG, because then 
        the sum of the moment of the full thrust and the aircraft mass has to be compensated by the HTP.
        minimum fwd posCoG has to be considered.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        mLM = self.parent.aircraft.mLM.getValue()
        cLMAXht = self.parent.cLMAXht.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingcM0L = self.parent.aircraft.wing.cM0L.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        DPR = self.parent.DPR.getValue()
        zEngine = -(self.parent.aircraft.engine.zEngine.getValue())   #zEngine is defined in VAMPzero as a negative value, but for the following equilibrium of 
                                                                      #the moments, a positive value of zEngine is needed for engines, which are installed
                                                                      #below the wing 
        wsL = self.parent.aircraft.wsL.getValue()
        cLL = self.parent.aircraft.cLL.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()

        #Stall speed Calculation
        vL = sqrt(2 * wsL * 9.81 / (rhoAP * cLL))*1.2 #Eq. 3.1 from Roskam I p-90

        qL = rhoAP/2 * vL**2
        qHTP_L = DPR * qL
        
        thrust_GoA = self.parent.aircraft.engine.thrustTO.getValue()              #Assumption: Thrust for GoAround is equal to the maximum thrust for Maximum TOM,
                                                                       #even for less weight configurations

        mu = 0.025

        # The current Landing Mass has to be smaller than the permitted landing mass
        # To enable vector operations we run the if statement on array level and then delete the according elements
        elementsNotToConsider = np.where(self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay[self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay>mLM])
        posCoGMIN = np.delete(self.parent.aircraft.posCoGMAX.posCoGMIN_fuel_pay, elementsNotToConsider)
        posCoGMAX = np.delete(self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay, elementsNotToConsider)
        m_TOW_fuel_pay = np.delete(self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay, elementsNotToConsider)

        if zEngine >= 0:    #Engines are installed below the wing, here in this contemplation of the direction of moments
            refAreaGoAround_var_max = (qL)/(qHTP_L * cLMAXht * lHT) * ((m_TOW_fuel_pay * 9.81)/(qL * wingrefArea)
                                    * (posCoGMAX - wingxMAC25) + wingcM0L * wingcMAC
                                    + (thrust_GoA * nEngine * zEngine)/(qL * wingrefArea)) * wingrefArea
            refAreaGoAround_var_min = (qL)/(qHTP_L * (-cLMAXht) * lHT) * ((m_TOW_fuel_pay* 9.81)/(qL * wingrefArea)
                                    * (posCoGMIN - wingxMAC25) + wingcM0L * wingcMAC
                                    + (thrust_GoA * nEngine * zEngine)/(qL * wingrefArea)) * wingrefArea
        else:               #Engines are installed above the wing
            cLMAXht = -cLMAXht
            refAreaGoAround_var_min = (qL)/(qHTP_L * cLMAXht * lHT) * ((m_TOW_fuel_pay * 9.81)/(qL * wingrefArea)
                                        * (posCoGMIN - wingxMAC25) + wingcM0L * wingcMAC
                                        + (thrust_GoA * nEngine * zEngine)/(qL * wingrefArea)) * wingrefArea
            refAreaGoAround_var_max = (qL)/(qHTP_L * cLMAXht * lHT) * ((m_TOW_fuel_pay * 9.81)/(qL * wingrefArea)
                                        * (posCoGMAX - wingxMAC25) + wingcM0L * wingcMAC
                                        + (thrust_GoA * nEngine * zEngine)/(qL * wingrefArea)) * wingrefArea

        refAreaGoAround_min = refAreaGoAround_var_min.max()
        refAreaGoAround_max = refAreaGoAround_var_max.max()
        refAreaGoAround = max(refAreaGoAround_min,refAreaGoAround_max)
        return refAreaGoAround
