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
from cmath import pi, cos, sin

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class mFuelRES(parameter):
    '''
    The fuel used in the reserve segment

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelRES, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the fuel mass used in the reserve segment. This is a simplified approach to the reserve fuel mass needed.
        It takes into account a climb from FL1500 to cruise altitude and a cruise to alternate for 200nm

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        :Source: Getting to Grips with Aircraft Performance, N.N., Airbus, 2002, pp. 174

        .. todo::

           Currently there is no holding implemented in this method
        '''

        #===============================================================================
        #Getting Values from Parameters
        #===============================================================================
        #@note: Set Cruise Distance to Alternate to 200nm
        distALT = 370000.

        mFuelCLIMB = self.parent.aircraft.fuel.mFuelCLIMB.getValue()
        mFuelCR = self.parent.aircraft.fuel.mFuelCR.getValue()
        mFuelTO = self.parent.aircraft.fuel.mFuelTO.getValue()
        mFuelDESCENT = self.parent.aircraft.fuel.mFuelDESCENT.getValue()
        mFM = self.parent.aircraft.fuel.mFM.getValue()

        #get Engine Data
        sfcCR = self.parent.aircraft.engine.sfcCR.getValue()
        sfcCLIMB = 0.07 #@todo: Urgently need SFC for climb

        #get Atmosphere Data
        q = self.parent.aircraft.atmosphere.qCR.getValue()
        rhoT = self.parent.aircraft.atmosphere.rhoCR.getValue()
        rhoB = self.parent.aircraft.atmosphere.rhoFL1500.getValue()
        sigmaB = self.parent.aircraft.atmosphere.sigmaFL1500.getValue()
        tasT = self.parent.aircraft.atmosphere.TASCR.getValue()
        IAS = self.parent.aircraft.IASCLIMB.getValue()
        time = self.parent.aircraft.timeCLIMB.getValue()
        gamma = self.parent.aircraft.gammaCLIMB.getValue()

        #get Aero Data
        cD0 = self.parent.aircraft.cD0.getValue()
        oswald = self.parent.aircraft.oswald.getValue()
        cDMINoffset = self.parent.aircraft.wing.cDMINoffset.getValue()

        #get Wing Data
        refArea = self.parent.aircraft.wing.refArea.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()

        #get Mass Data
        oEM = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()

        #=======================================================================
        # Climb Segment
        #=======================================================================
        #T is the indice for top, B for bottom!
        mB = oEM + mPayload + self.getValue()
        #@todo: calc mFuelRES: Mass at top of climb
        mT = mB

        tasB = IAS * sigmaB
        mFuelClimb = 0.
        if rhoT != 0. and rhoB != 0. and tasT != 0. and tasB != 0. and refArea != 0. and aspectRatio != 0. and oswald != 0.:
            cLT = mT * 9.81 / (0.5 * rhoT * tasT ** 2 * refArea) * cos(gamma * rad)
            cLB = mB * 9.81 / (0.5 * rhoB * tasB ** 2 * refArea) * cos(gamma * rad)

            cDT = cD0 + cLT * cDMINoffset + cLT ** 2 / (pi * aspectRatio * oswald)
            cDB = cD0 + cLB * cDMINoffset + cLB ** 2 / (pi * aspectRatio * oswald)

            #thrust equals drag taking gamma into account
            dragT = 0.5 * rhoT * tasT ** 2 * refArea * cDT
            dragB = 0.5 * rhoB * tasB ** 2 * refArea * cDB

            #neglecting fuel loss during climb?!
            thrT = dragT + mT * sin(gamma * rad) * 9.81
            thrB = dragB + mB * sin(gamma * rad) * 9.81

            mFuelClimb = time / 3600. * (thrT + thrB) / (2.) * sfcCLIMB

        #=======================================================================
        # Cruise to alternate
        #=======================================================================

        #Initialize
        massCurrent = oEM + mPayload + self.getValue()
        fuelAvailable = mFM - mFuelTO - mFuelCLIMB - mFuelDESCENT - mFuelCR
        fuelResult = 0.
        remainDist = distALT

        #Distance for iteration
        it = 10000

        #Fly Segments
        while remainDist >= 0. and q != 0. and oswald != 0. and refArea != 0. and aspectRatio != 0. and fuelAvailable > 0. and massCurrent > 0. and sfcCR > 0. and tasT != 0:
            cLCurrent = massCurrent * 9.81 / (q * refArea)
            cDCurrent = cD0 + cLCurrent * cDMINoffset + cLCurrent ** 2 / (pi * aspectRatio * oswald)
            thrustReq = cDCurrent * q * refArea
            timeSeg = it / tasT
            fuelSeg = timeSeg / 3600. * thrustReq * sfcCR#/9.81
            massCurrent = massCurrent - fuelSeg
            remainDist = remainDist - it
            fuelAvailable = fuelAvailable - fuelSeg
            fuelResult = fuelResult + fuelSeg
            #@todo: calc mFuelRes currently not adding the mFuelClimb Check this
        return self.setValueCalc(fuelResult + mFuelClimb)