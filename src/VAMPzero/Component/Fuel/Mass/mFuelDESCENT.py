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

rad = pi / 180.


class mFuelDESCENT(parameter):
    '''
    The fuel used in the descent segment

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelDESCENT, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                           cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the fuel mass for the descent segment.

        The descent segment is initialized at cruise altitude and continues down to FL1500. Masses and atmosphere
        data at these locations are taken into account. Equilibrium of forces is then applied to find the necessary thrust
        and calculate the needed fuel mass.

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        :Source: Getting to Grips with Aircraft Performance, N.N., Airbus, 2002, pp. 159
        '''
        #T is the indice for top, b for bottom!
        rhoT = self.parent.aircraft.atmosphere.rhoCR.getValue()
        rhoB = self.parent.aircraft.atmosphere.rhoFL1500.getValue()
        sigmaB = self.parent.aircraft.atmosphere.sigmaFL1500.getValue()
        tasT = self.parent.aircraft.atmosphere.TASCR.getValue()

        IAS = self.parent.aircraft.IASDESCENT.getValue()
        time = self.parent.aircraft.timeDESCENT.getValue()

        #get Aero Data
        cD0 = self.parent.aircraft.cD0.getValue()
        oswald = self.parent.aircraft.oswald.getValue()
        cDMINoffset = self.parent.aircraft.wing.cDMINoffset.getValue()

        #get Wing Data
        refArea = self.parent.aircraft.wing.refArea.getValue()
        aspectRatio = self.parent.aircraft.wing.aspectRatio.getValue()

        SFCLoi = self.parent.aircraft.engine.sfcLOI.getValue()

        oEM = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()
        mFuelDESCENT = self.getValue()

        mFuelCLIMB = self.parent.aircraft.fuel.mFuelCLIMB.getValue()
        mFuelCR = self.parent.aircraft.fuel.mFuelCR.getValue()
        mFuelTO = self.parent.aircraft.fuel.mFuelTO.getValue()
        mFM = self.parent.aircraft.fuel.mFM.getValue()

        m = oEM + mPayload + mFM - mFuelTO - mFuelCLIMB - mFuelCR - mFuelDESCENT

        tasB = IAS * sigmaB

        if rhoT != 0. and rhoB != 0. and tasT != 0. and tasB != 0. and refArea != 0. and aspectRatio != 0. and oswald != 0.:
            #thrust equals drag taking gamma into account
            cLT = (m + mFuelDESCENT) * 9.81 / (0.5 * rhoT * tasT ** 2 * refArea)
            cLB = (m) * 9.81 / (0.5 * rhoB * tasB ** 2 * refArea)

            cDT = cD0 + cLT * cDMINoffset + cLT ** 2 / (pi * aspectRatio * oswald)
            cDB = cD0 + cLB * cDMINoffset + cLB ** 2 / (pi * aspectRatio * oswald)

            dragT = 0.5 * rhoT * tasT ** 2 * refArea * cDT
            dragB = 0.5 * rhoB * tasB ** 2 * refArea * cDB

            #@todo: think about this!!!
            thrT = dragT #tan(gamma*rad)  *
            thrB = dragB#tan(gamma*rad)  *

            mFuel = time / 3600. * (thrT + thrB) / (2.) * SFCLoi

            return self.setValueCalc(mFuel)