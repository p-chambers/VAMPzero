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


class refAreaTakeOff(parameter):
    '''
    The reference area for the vertical tailplane for the Take Off.
    
    :Unit: [m2]

    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refAreaTakeOff, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)


    def calc(self):
        '''
        Calculates the reference area for the VTP from the maximum value of the different calculations.
        '''
        refAreaControl = self.calcControl()
        refAreaTakeOff = refAreaControl

        return self.setValueCalc(refAreaTakeOff) 
                
    def calcControl(self):
        '''
        Calculates the reference area for the VTP from the moment of equilibrium as a result of one engine failure (OEI). The VTP has to compensate the
        remaining thrust from the active engine and additional the drag from the inactive engine.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''   
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        aAP = self.parent.aircraft.atmosphere.aAP.getValue()
        lVT = self.parent.lVT.getValue()
        aspectRatioVPT = self.parent.aspectRatio.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()
        oswald = self.parent.aircraft.wing.oswald.getValue()
        phi50VTP = self.parent.phi50.getValue()
        cD0 = self.parent.aircraft.cD0.getValue()
        dCDTO = self.parent.aircraft.wing.flap.dCDTO.getValue()        
        dCDextendedLG = self.parent.aircraft.landingGear.dCDextendedLG.getValue()
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        yEngine = self.parent.aircraft.engine.yEngine.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        cLTO = self.parent.aircraft.cLTO.getValue()
        refArea = self.parent.aircraft.wing.refArea.getValue()

        g = 9.81
        vs = sqrt(2 * mTOM * g / (rhoAP * cLTO * refArea))
        v1 = vs
        v2 = 1.2 * vs

        #m_TOW, posCoG_fuel_pay_nt,posCoG_fuel_pay_tn,posCoG_fuel,m_PAX,posCoGMIN_fuel_pay0, posCoGMIN_fuel_pay, posCoGMAX_fuel_pay0,posCoGMAX_fuel_pay,m_TOW_fuel_pay = self.parent.aircraft.posCoGMAX.massTable()
        x1 = self.parent.aircraft.sTOFL.x1

        machTO = v2/aAP
        qTO = rhoAP/2 * v2**2
        
        length_m_TOW_fuel_pay = len(self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay)
        
        cLTO_var = np.zeros((length_m_TOW_fuel_pay,1))
        cDTO_var = np.zeros((length_m_TOW_fuel_pay,1))
        thrust_TO_var = np.zeros((length_m_TOW_fuel_pay,1))
        beta_var = np.zeros((length_m_TOW_fuel_pay,1))
        refAreaControl_var = np.zeros((length_m_TOW_fuel_pay,1))

        Phi = 5                     # in [deg], maximum value according to the regulation of FAA
        zeta = 25                   # in [deg], maximum value
        c_Q_beta_profile = 6.1416   # in [1/rad], for the VTP profile
        C_Q_zeta = 1.0616           # in [1/rad]
        
        kappaVTP = c_Q_beta_profile * (1 - machTO**2)/(2 * pi)
        kappaVTP = kappaVTP.real
        C_Q_beta = (2 * pi * aspectRatioVPT)/(2 + sqrt(aspectRatioVPT**2/kappaVTP**2 * (tan(phi50VTP*pi/180)**2 + 1 - machTO**2) + 4)) #in [1/rad], for the VTP
        C_Q_beta = C_Q_beta.real

        mu = 0.025
        
        cLTO_var = (2 * self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81)/(rhoAP * v2**2 * wingrefArea)
        cDTO_var = cD0 + dCDTO + dCDextendedLG + cLTO_var**2/(pi * aspectRatio * oswald)
        beta_var = -cLTO_var / C_Q_beta * Phi
        beta_var = beta_var.real
        #Assumption: Thrust equals roll drag, aerodynamic drag and acceleration to v1 in x1
        #additional drag from the inoperative engine (factor 1.25 for windmilling fan with big BPR), estimation by Scholz, Dieter: 
        #Skript zur Vorlesung Flugzeugentwurf, Hochschule fuer Angewandte Wissenschaften Hamburg, 1999            
        thrust_TO_var = 1.25 * (mu * self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * 9.81 + rhoAP/2 * v1**2 * cDTO_var * wingrefArea + self.parent.aircraft.posCoGMAX.m_TOW_fuel_pay * v1**2/(2* x1))/ nEngine
        refAreaControl_var = (thrust_TO_var * yEngine)/(qTO * lVT * (-C_Q_beta * beta_var * pi/180 + C_Q_zeta * zeta * pi/180))

        refAreaControl = refAreaControl_var.max()
        return refAreaControl
