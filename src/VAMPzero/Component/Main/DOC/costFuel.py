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
from VAMPzero.Handler.Parameter import parameter

class costFuel(parameter):
    '''
    The mission fuel costs per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costFuel, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates fuel costs per flight hour for the mission

        
        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf          
        '''
        
        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()                # Exchange rate dollar to euro [EU/$]
        priceFuel = self.parent.priceFuel.getValue()                            # Fuel price [$/kg]
        mFM = self.parent.fuel.mFM.getValue()                                   # Mission fuel mass [kg]    
        tFlight = self.parent.tFlight.getValue()                                # Flight time of typical mission [hr]
        
        costFuel = (USDexchangeEURO * priceFuel * mFM) / tFlight                # Fuel cost [EU/hr]

        return self.setValueCalc(costFuel)                

    def calcDimchev(self):
        '''
        Calculates the fuel costs per flight hour for the mission
        
        :Source: adapted from DLR-LY-IL DOC Tool, S. Langhans, 2010
        :Author: Momchil Dimchev, TU Delft
        '''

        mBlock = self.parent.fuel.mFM.getValue()
        tFlight = self.parent.tFlight.getValue()
        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()
        PriceFuel = self.parent.priceFuel.getValue()

        FUEL = (mBlock * PriceFuel)

        return self.setValueCalc((FUEL / tFlight) * USDexchangeEURO)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======