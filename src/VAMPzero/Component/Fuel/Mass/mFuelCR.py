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

from math import pi

from VAMPzero.Handler.Parameter import parameter


class mFuelCR(parameter):
    '''
    The fuel used in the cruise segment

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelCR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        If the design range :ref:`aircraft.desRange` is fixed calcFixRange is chosen, if not the calcFixFuel() method is selected.
        '''
        if self.parent.mFM.getStatus() == 'fix':
            return self.calcFixFuel()
        elif self.parent.aircraft.desRange.getStatus() == 'fix':
            return self.calcFixRange()
        else:
            return self.calcFixRange()

    def calcFixRange(self):
        '''
        Calculates the fuel mass for the cruise segment if the range is given.

        The calculation is based on a simple equilibrium of forces approach. This means that this
        is a constant altitude cruise phase. An iteration cycle with a leg length of 10km is applied to
        find the needed fuel mass.

        The initial aircraft mass is determined from the actual takeoff mass minus the fuel mass for climb and takoff

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        :Source: Getting to Grips with Aircraft Performance, N.N., Airbus, 2002, pp. 129
        '''
        # get Fuel Data
        mFuelCLIMB = self.parent.aircraft.fuel.mFuelCLIMB.getValue()
        mFuelTO = self.parent.aircraft.fuel.mFuelTO.getValue()
        mFM = self.parent.aircraft.fuel.mFM.getValue()

        # get Distance Data
        distCR = self.parent.aircraft.distCR.getValue()

        # get Engine Data
        sfcCR = self.parent.aircraft.engine.sfcCR.getValue()

        # get Mass Data
        oWE = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()

        # get Atmosphere Data
        q = self.parent.aircraft.atmosphere.qCR.getValue()
        TAS = self.parent.aircraft.atmosphere.TASCR.getValue()

        # get Aero Data
        cDw = self.parent.aircraft.wing.cDw.getValue()
        cDMINoffset = self.parent.aircraft.wing.cDMINoffset.getValue()
        cD0 = self.parent.aircraft.cD0.getValue()
        oswald = self.parent.aircraft.oswald.getValue()

        # get Wing Data
        refArea = self.parent.aircraft.wing.refArea.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()


        # Initialize
        massCurrent = oWE + mPayload + mFM - mFuelCLIMB - mFuelTO
        fuelResult = 0
        remainDist = distCR

        # Distance for iteration
        it = 10000

        # Fly Segments
        while remainDist >= 0. and q != 0. and oswald != 0. and refArea != 0. and aspectRatio != 0. and massCurrent > 0. and sfcCR > 0.:
            cLCurrent = massCurrent * 9.81 / (q * refArea)
            cDCurrent = cDw + cD0 + cLCurrent * cDMINoffset + cLCurrent ** 2 / (pi * aspectRatio * oswald)
            thrustReq = cDCurrent * q * refArea
            timeSeg = it / TAS
            fuelSeg = timeSeg / 3600. * thrustReq * sfcCR
            massCurrent = massCurrent - fuelSeg
            remainDist = remainDist - it
            fuelResult = fuelResult + fuelSeg

        return self.setValueCalc(fuelResult)

    def calcFixFuel(self):
        '''
        Calculates the fuel mass for a cruise segment if the
        fuel mission fuel mass is fixed.

        Since the mission fuel mass is fixed, the fuel mass for the cruise phase is
        limited by the fuel needed in all other segments of the mission.

        :Source: Daniel Boehnke
        '''
        # get Fuel Data
        mFuelCLIMB = self.parent.aircraft.fuel.mFuelCLIMB.getValue()
        mFuelTO = self.parent.aircraft.fuel.mFuelTO.getValue()
        mFuelRES = self.parent.aircraft.fuel.mFuelRES.getValue()
        mFuelDESCENT = self.parent.aircraft.fuel.mFuelDESCENT.getValue()
        mFM = self.parent.aircraft.fuel.mFM.getValue()

        fuelAvailable = mFM - mFuelTO - mFuelCLIMB - mFuelDESCENT - mFuelRES
        
        if fuelAvailable < 0.: 
            self.log.warning('VAMPzero FUEL: The remaining fuel for the cruise segment is not sufficient for any cruise!')
        
        return self.setValueCalc(fuelAvailable)

