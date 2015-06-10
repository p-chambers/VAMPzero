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


class costInterest(parameter):
    '''
    The interest costs per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costInterest, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                           cpacsPath=cpacsPath)

    def calc(self):
        '''
        The calculation method stems from the QUICE project. As the interest cost are included in the annuity that is also influenced by 
        the depreciation period, this calculation simply sets the interest cost to zero. See the corresponding calculation method
        for costDepreciation for further information. 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        return self.setValueCalc(0.)

    def calcKundu(self):
        '''
        Calculates the interest costs per flight hour
        
        The calculation is simplified by assuming that the total capital cost are similar to the aircraft price
        
        :Source: Aircraft Design, A. Kundu, 2010, p.546
        '''

        priceAC = self.parent.priceAircraft.getValue()
        utilization = self.parent.utilization.getValue()
        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()

        cost = 0.053 * USDexchangeEURO * priceAC / utilization

        return self.setValueCalc(cost)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======