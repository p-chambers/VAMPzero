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
from cmath import sqrt, pi

from VAMPzero.Handler.Parameter import parameter


class sTOFLISA(parameter):
    '''
    The take-off field length for ISA standart conditions at sea level
    
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(sTOFLISA, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)


    def calc(self):
        '''
        Calculates the takeoff field length for the following cases:
        
        * normal takeoff
        * OEI aborted takeoff
        * OEI continued takeoff
        
        Returns the balanced field length. 
        
        :Source: Flugzeugentwurf I Vorlesungsskript, V. Gollnick 
        '''

        def thrustAtV(thrustTO, v):
            #the thrust a 100m/s is roughly 0.85 of the initial thrust
            return thrustTO * (1 - v * 0.0015)

        # Initialisation
        mTOM = self.parent.mTOM.getValue()
        thrustTOISA = self.parent.engine.thrustTOISA.getValue()
        refArea = self.parent.wing.refArea.getValue()
        rho = self.parent.atmosphere.rhoA[0]
        cLTO = self.parent.cLTO.getValue()
        cD0 = self.parent.cD0.getValue()
        dCDTO = self.parent.wing.flap.dCDTO.getValue()
        dCDextendedLG = self.parent.landingGear.dCDextendedLG.getValue()
        dCDOEI = self.parent.engine.dCDOEI.getValue()
        oswald = self.parent.oswald.getValue()
        aspectRatio = self.parent.wing.aspectRatio.getValue()
        nEngine = self.parent.engine.nEngine.getValue()

        thrustTO = thrustTOISA * nEngine

        #coefficients
        mu = 0.03
        g = 9.81
        qS = .05 * rho * refArea

        #field length values initialization
        x1 = 0.
        x2 = 51.
        x3 = 0.
        x4 = 0.
        x5 = 0.
        nIter = 0.

        # Velocities
        vs = sqrt(2 * mTOM * g / (rho * cLTO * refArea))
        v1 = vs
        vR = 1.1 * vs
        v2 = 1.2 * vs

        # Need to reset these to real numbers to enable comparisons.
        try:
            vs = vs.real
            v1 = v1.real
        except:
            pass

        # To calculate the balanced field length the velocity v1 is increased
        # until the length for aborted and continued takeoff for OEI are equal. 
        # As a lot of non-sense can occur in the early iterations of VAMPzero
        # some additional break criteria like e.g. nIter are introduced here.
        while abs(x2 + x3 - x4 - x5) > 1. and nIter < 100. and v1 < 1.2 * vs:
            # Thrust
            thrust0 = thrustTO
            thrust1 = thrustAtV(thrustTO, v1)
            thrustR = thrustAtV(thrustTO, vR)
            thrust2 = thrustAtV(thrustTO, v2)

            thrust1OEI = thrust1 * (nEngine - 1.) / nEngine
            thrustROEI = thrustR * (nEngine - 1.) / nEngine
            thrust2OEI = thrust2 * (nEngine - 1.) / nEngine

            # Aerodynamics
            cLTO1 = cLTO / 1.1 ** 2.
            cLTO2 = cLTO / 1.2 ** 2.

            cDTO = cD0 + dCDextendedLG + dCDTO + cLTO ** 2 / (pi * oswald * aspectRatio)
            cDTOOEI = cDTO + dCDOEI
            cDTO1 = cD0 + dCDextendedLG + dCDTO + cLTO1 ** 2 / (pi * oswald * aspectRatio)
            cDTOOEI1 = cDTO1 + dCDOEI
            cDTO2 = cD0 + dCDextendedLG + dCDTO + cLTO2 ** 2 / (pi * oswald * aspectRatio)
            cDTOOEI2 = cDTO2 + dCDOEI

            # Accelerations in longitudinal direction
            a0 = (thrust0 - mu * (mTOM * g)) / mTOM
            a1 = (thrust1 - mu * (mTOM * g - cLTO1 * qS * v1 ** 2) - cDTO1 * qS * v1 ** 2) / mTOM
            a1OEI = (thrust1OEI - mu * (mTOM * g - cLTO1 * qS * v1 ** 2) - cDTOOEI1 * qS * v1 ** 2) / mTOM
            aR = (thrustR - mu * (mTOM * g - cLTO1 * qS * vR ** 2) - cDTO1 * qS * vR ** 2) / mTOM
            aROEI = (thrustROEI - mu * (mTOM * g - cLTO1 * qS * vR ** 2) - cDTOOEI1 * qS * vR ** 2) / mTOM
            a2 = (thrust2 - mu * (mTOM * g - cLTO2 * qS * v2 ** 2) - cDTO2 * qS * v2 ** 2) / mTOM
            a2OEI = (thrust2OEI - mu * (mTOM * g - cLTO2 * qS * v2 ** 2) - cDTOOEI2 * qS * v2 ** 2) / mTOM

            #Initial roll distance
            x1 = v1 ** 2. / (2 * (0.3 * a0 + 0.7 * a1))

            #=======================================================================
            # Aborted takeoff OEI
            #=======================================================================
            # Dead time for 4s
            vb = v1 + a1OEI * 4.
            x2 = (vb ** 2 - v1 ** 2) / (2 * a1OEI)

            # Breaking
            ab = 0.35 * g
            x3 = vb ** 2 / (2. * ab)

            #=======================================================================
            # Continued takeoff with OEI
            #=======================================================================
            # Accelleration to v2
            x4 = (v2 ** 2 - v1 ** 2) / (2. * (0.3 * a1OEI + 0.7 * a2OEI))

            # Climb out at v2 to reach Hs of 35ft
            gamma = (thrust2OEI / (mTOM * g)) - (cDTOOEI2 / (cLTO2))
            Hs = 0.3048 * 35.
            x5 = Hs / gamma

            # to run the loop increase values
            v1 = v1 + 0.5
            nIter = nIter + 1

            # Cmath operations do return complex values. Need to reset these to 
            # enable the comparisons in the while loop
            try:
                vs = vs.real()
                v1 = v1.real()
            except:
                pass

        return self.setValueCalc(x1 + x2 + x3)
