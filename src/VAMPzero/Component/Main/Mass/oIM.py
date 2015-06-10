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


class oIM(parameter):
    '''
    The operator's mass definition equals the Airbus weight 
    chapter 60 and 61. The operator's items mass includes the removable part of 
    the cabin arrangement, the emergency equipment, catering, fluids aircraft 
    documents, tool kit and the crew. Please note, that the formula below is developed 
    for typical passenger aircraft and not for aircraft having a pure business 
    or VIP cabin layout! The mass definition is broken down as follows:
    
    * standard items

       * unusable fuel
       * A/C documents and tool kit
       * galley structure
       * passenger seats
       * removable crew rest
       * additional center tank (in the cargo compartment)
       * seat mounted electronical system (in-flight entertainment)
       
    * operational items 

       * emergency equipment 
       * water for galleys and toilets (incl. the water in the tanks)
       * fluid for toilets (waste tank precharge)
       * (usable) engine and APU oil
       * catering
       * crew
    
    The mass definition between the Airbus accounting and the 
    DIN 9020 (which is normally used within LTH) is similar to 
    the sum of the DIN9020 chapters 40, 18 and 20, but 
    differs in several points. The operators items weight 
    of the Fokker F100 is ~4.5% higher according to the DIN 
    9020 definition than according to the Airbus definition.

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(oIM, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the operators item mass from the class layout and the number of passengers 
        
        :Source: LTH UL-442.0(T). 
        '''
        paxSeats = self.parent.payload.paxSeats.getValue()
        nClasses = self.parent.fuselage.nClasses.getValue()

        if nClasses <= 2:
            self.setDeviation(0.063) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
            
            return self.setValueCalc(32.907 * paxSeats ** 1.021)

        elif nClasses == 3:
            self.setDeviation(0.051) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
            
            return self.setValueCalc(35.782 * paxSeats ** 1.1141)

        else:
            self.log.warning("VAMPzero Calc: Missing suitable class layout in calc oIM")

    def calcDorbath(self):
        '''
        Calculates operator items weight 
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 139
        '''
        paxSeats = self.parent.payload.paxSeats.getValue()

        if self.parent.rangeType.getValue() >= 1:
            return self.setValueCalc(40.863 * paxSeats - 521.84)
        elif self.parent.rangeType.getValue() == 0:
            return self.setValueCalc(74.353 * paxSeats - 1917.6)
        else:
            self.log.error("in calcOperatorItemsFelix no valid value for ShortRange Switch")

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
