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

from cmath import pi, sin, cos

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class mFuelCLIMB(parameter):
    '''
    The fuel used in the climb segment

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelCLIMB, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the fuel mass for the climb segment. This is a simplified version of Joerg Fuchte's implementation.

        The climb segment is initialized at FL1500 and continues up the cruise altitude. Masses and atmosphere
        data at these locations are taken into account. Equilibrium of forces is then applied to find the necessary thrust
        and calculate the needed fuel mass. Currently the SFC for the climb phase is only guess work

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        :Source: Getting to Grips with Aircraft Performance, N.N., Airbus, 2002, pp. 149

        .. todo::

           Urgently need SFC for climb
        '''
        #T is the indice for top, b for bottom!
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

        #@todo: Urgently need SFC for climb
        sfcCLIMB = 0.07

        oEM = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()
        mFuelM = self.parent.mFM.getValue()
        mFuelTO = self.parent.mFuelTO.getValue()
        mFuelCLIMB = self.getValue()

        mB = oEM + mPayload + mFuelM - mFuelTO
        mT = oEM + mPayload + mFuelM - mFuelTO - mFuelCLIMB

        #tasT        = IAS * sigmaT
        tasB = IAS * sigmaB

        if rhoT != 0. and rhoB != 0. and tasT != 0. and tasB != 0. and refArea != 0. and aspectRatio != 0. and oswald != 0.:
            #thrust equals drag taking gamma into account
            cLT = mT * 9.81 / (0.5 * rhoT * tasT ** 2 * refArea) * cos(gamma * rad)
            cLB = mB * 9.81 / (0.5 * rhoB * tasB ** 2 * refArea) * cos(gamma * rad)

            cDT = cD0  + cLT * cDMINoffset + cLT ** 2 / (pi * aspectRatio * oswald)
            cDB = cD0  + cLB * cDMINoffset + cLB ** 2 / (pi * aspectRatio * oswald)

            #thrust equals drag taking gamma into account
            dragT = 0.5 * rhoT * tasT ** 2 * refArea * cDT
            dragB = 0.5 * rhoB * tasB ** 2 * refArea * cDB

            #neglecting fuel loss during climb?!
            thrT = dragT + mT * sin(gamma * rad) * 9.81
            thrB = dragB + mB * sin(gamma * rad) * 9.81

            mFuel = time / 3600. * (thrT + thrB) / (2.) * sfcCLIMB

            return self.setValueCalc(mFuel)