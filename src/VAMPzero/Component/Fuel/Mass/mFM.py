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
from math import e

from VAMPzero.Handler.Parameter import parameter


class mFM(parameter):
    '''
    The complete mission fuel mass 
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFM, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the calc method. If the :ref:`aircraft.mTOM` is fixed calcMass is chosen. If the :ref:`aircraft.desRange` is fixed calcSum is chosen. 
        '''

        if self.parent.aircraft.mTOM.getStatus() == 'fix':
            self.calc = self.calcMass
        elif self.parent.aircraft.desRange.getStatus() == 'fix':
            self.calc = self.calcSum
        elif self["status"] != 'fix':
            self.log.warning(
                "VAMPzero Calc: Neither mTOM nor desRange nor mFM are fixed. Performance analysis will probably not converge")


    def calcSum(self):
        '''
        Calculate the fuel needed for the complete mission via the sum of all mission segment fuel masses  
        '''

        mFuelCLIMB = self.parent.mFuelCLIMB.getValue()
        mFuelDESCENT = self.parent.mFuelDESCENT.getValue()
        mFuelCR = self.parent.mFuelCR.getValue()
        mFuelTO = self.parent.mFuelTO.getValue()
        mFuelRES = self.parent.mFuelRES.getValue()

        return self.setValueCalc(mFuelCLIMB + mFuelCR + mFuelDESCENT + mFuelRES + mFuelTO)

    def calcMass(self):
        '''
        Calculates the mission fuel mass from the maximum takeoff mass and the operating empty weight and payload
        '''
        self.setDeviation(0.1465) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        mTOM = self.parent.aircraft.mTOM.getValue()
        oEM = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()

        return self.setValueCalc(mTOM - oEM - mPayload)

    def calcRaymer(self):
        '''
        Calculate the fuel needed for the complete mission via Brequet equation and fuel fractions
         
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 19
        
        '''
        vTAS = self.parent.aircraft.atmosphere.TASCR.getValue()
        Range = self.parent.aircraft.desRange.getValue()
        SFC = self.parent.aircraft.engine.sfcCR.getValue()
        LoDcr = self.parent.aircraft.loDCR.getValue()
        ResTime = self.parent.aircraft.timeRES.getValue()
        SFCloi = self.parent.aircraft.engine.sfcLOI.getValue()
        LoDloi = self.parent.aircraft.loDLOI.getValue()
        oEM = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()
        mFM = self.getValue()

        TOM = mFM + mPayload + oEM
        TOWzuLDWtoclcrla = e ** (-1 * Range * 1000. * (SFC / 3600.) / (vTAS * LoDcr) / 0.951)
        TOWzuLDWloi = e ** (-1 * ResTime * SFCloi / LoDloi)
        FuelWeight = (1 - TOWzuLDWtoclcrla * TOWzuLDWloi) * TOM

        return self.setValueCalc(FuelWeight)

    def calcViaRange(self):
        '''
        Calculates the mission fuel mass for for an 
        electric airplane where no mission fuel is lost during cruise
        
        :Author: Marco Friederich, TU Braunschweig
        
        .. todo:: 
        
           missing Source calcViaRange mFM
        '''
        desRange = self.parent.aircraft.desRange.getValue()
        cdCruise = self.parent.aircraft.cDCR.getValue()
        q = self.parent.aircraft.atmosphere.qCR.getValue()
        refArea = self.parent.aircraft.wing.refArea.getValue()
        oEM = self.parent.aircraft.oEM.getValue()
        mFM = self.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()
        LoDcr = self.parent.aircraft.loDCR.getValue()
        eta = 0.4

        if cdCruise == 0:
            return self.setValueCalc(5)

        F = q * cdCruise * refArea

        result = ((F + (oEM + mPayload + mFM) * 9.81 / LoDcr) * (desRange * 1000) / eta / (43.5 * 1000000))
        
        return self.setValueCalc(result)
