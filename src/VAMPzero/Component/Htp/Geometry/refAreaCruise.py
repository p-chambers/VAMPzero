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


class refAreaCruise(parameter):
    '''
    The reference area of the horizontal tailplane
    
    :Unit: [m2]

    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis    
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refAreaCruise, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reference area for the HTP from the maximum value of the different calculations.
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        machCR = self.parent.aircraft.machCR.getValue()
        aCR = self.parent.aircraft.atmosphere.aCR.getValue()
        rhoCR = self.parent.aircraft.atmosphere.rhoCR.getValue()
        DPR = self.parent.DPR.getValue()

        delta_MMO = 0.05                 # margin to Maximum Operating Mach Number (MMO) may not less than 0.05
        self.machCr_MMO = machCR + delta_MMO  # (Source: FAR 25.335: Design airspeeds, FAR 25.253 High-speed characteristics)
        self.vCR_MMO = self.machCr_MMO * aCR
        self.qCR_MMO = rhoCR/2 * self.vCR_MMO**2
        self.qHTP_CR = DPR * self.qCR_MMO

        refAreaStability = self.calcStability()
        refAreaControl = self.calcControl()

        try:  # in any case of complex values (with +- 0j) guarantee for real values
            refAreaStability = refAreaStability.real
            refAreaControl = refAreaControl.real
        except ValueError:
            self.log.debug('VAMPzero CALC: Could not convert HTP areas to real')

        refAreaCruise = max(refAreaStability,refAreaControl)
        return self.setValueCalc(refAreaCruise)

    def calcStability(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the cruise phase.
        It is calculated the area of the HTP, for which the aircraft is natural stable in case of the maximum aft posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        aspectRatioWing = self.parent.aircraft.wing.aspectRatio.getValue() 
        phi50Wing = self.parent.aircraft.wing.phi50.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        xMAChtp = self.parent.xMAC.getValue()
        static_margin = self.parent.aircraft.static_margin.getValue()        
        CLalphaHTP = self.parent.CLalphaHTP_CR.getValue()
        machCR_MMO = self.machCr_MMO
        qCR_MMO = self.qCR_MMO
        qHTP_CR = self.qHTP_CR
        dalphaW_dalpha = self.parent.detadalpha.getValue()

        x = xMAChtp - wingxMAC25
        
        delta_posCoG_rel = 2.                              #additional posCoG in order to consider the CG-Range while cruising, in [%] of cMAC
        delta_posCoG = (delta_posCoG_rel/100)*wingcMAC     #in absolute value
        
        CLalphaWing = (2 * pi * aspectRatioWing)/(2 + (aspectRatioWing**2 * (tan(phi50Wing*pi/180)**2 + 1 - machCR_MMO**2) + 4)**0.5)
        CLalphaWing = CLalphaWing.real

        posCoGMAX = self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay + delta_posCoG
        refAreaStability_var = wingrefArea * (qCR_MMO/qHTP_CR) * (CLalphaWing*(posCoGMAX - wingxMAC25
                                  - static_margin*wingcMAC)) / (CLalphaHTP*(1 - dalphaW_dalpha)*(lHT - posCoGMAX
                                  + wingxMAC25 + static_margin*wingcMAC))
        
        refAreaStability = refAreaStability_var.max()
        
        if refAreaStability < 0:
            refAreaStability = 1.
        
        return refAreaStability  
       
    def calcControl(self):
        '''
        Calculates the reference area for the HTP from the equilibrium of the moments during the cruise phase.
        It is calculated the area of the HTP, so that the aircraft can be stabilized in case of the minimum fwd posCoG.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        cLMAXht = self.parent.cLMAXht.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        wingcMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        lHT = self.parent.lHT.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()
        oswald = self.parent.aircraft.wing.oswald.getValue()
        wingcm0 = self.parent.aircraft.wing.cM0CR.getValue()
        cD0 = self.parent.aircraft.cD0.getValue()
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        qCR_MMO = self.qCR_MMO
        qHTP_CR = self.qHTP_CR
        zEngine = -(self.parent.aircraft.engine.zEngine.getValue())   #zEngine is defined in VAMPzero as a negative value, but for the following equilibrium of
                                                                      #the moments, a positive value of zEngine is needed for engines, which are installed
                                                                      #below the wing 

        cLMAXht = -cLMAXht

        mCM = self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay                                #cruise mass, assumption that it's equal to the Take Off Mass

        delta_posCoG_rel = 2.                               #additional posCoG in order to consider the CG-Range while cruising, in[%]
        delta_posCoG = (delta_posCoG_rel/100)*wingcMAC      #in absolute value

        posCoGMIN = self.parent.aircraft.posCoGMAX.posCoGMIN_fuel_pay - delta_posCoG
        posCoGMAX = self.parent.aircraft.posCoGMAX.posCoGMAX_fuel_pay + delta_posCoG
        cLCR_var = (mCM * 9.81)/(qCR_MMO * wingrefArea)
        cDCR_var = cD0 + cLCR_var**2/(pi * aspectRatio * oswald)
        thrust_CR_var = qCR_MMO * cDCR_var * wingrefArea / nEngine    #Assumption: Drag equals thrust
        if zEngine > 0:     #The critical case for the htp, when the engines are installed below the wing (below the CoG), is without consideration of the thrust 
            thrustCR = thrust_CR_var * 0
        else:               #Engines above the wing (above the CoG), the moment of the thrust works against the rotation, the HTP has to be bigger
            thrustCR = thrust_CR_var
        refAreaControl_var_min = (qCR_MMO)/(qHTP_CR * cLMAXht * lHT) * ((mCM * 9.81)/(qCR_MMO * wingrefArea) 
                                    * (posCoGMIN - wingxMAC25) + wingcm0 * wingcMAC 
                                    + (thrustCR * nEngine * zEngine)/(qCR_MMO * wingrefArea)) * wingrefArea
        refAreaControl_var_max = (qCR_MMO)/(qHTP_CR * cLMAXht * lHT) * ((mCM * 9.81)/(qCR_MMO * wingrefArea) 
                                    * (posCoGMAX - wingxMAC25) + wingcm0 * wingcMAC 
                                    + (thrustCR * nEngine * zEngine)/(qCR_MMO * wingrefArea)) * wingrefArea
                                        
        refAreaControl_min = refAreaControl_var_min.max()
        refAreaControl_max = refAreaControl_var_max.min()
        refAreaControl = max(refAreaControl_min,refAreaControl_max)

        return refAreaControl
