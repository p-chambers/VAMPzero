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


class mFurn(parameter):
    '''
    The furnishings mass definition equals the Airbus weight chapter 50 to 54. 
    The furnishings mass includes the fixed part of the cabin and cargo arrangement, 
    the external decorative paint, the fixed oxygen, the internal and external 
    lighting and the water installation. Please note, that the formula below is developed 
    for typical passenger aircraft and not for aircraft having a pure business or 
    VIP cabin layout! The mass definition is broken down as follows:
    
    * furnishings

       * insulation
       * trim panels
       * crew seats and fixed crew rests
       * partitions, stowages, doors, monument lining
       * toilets
       * hatracks, bins
       * floor covering
       * cargo linings
       * cargo loading system
       * miscellaneous (door control panel, lifts, emergency ladder, external decorative paint)
       
    * emergency oxygen (in cockpit and cabin)
    * lighting (cockpit, cabin, service area, cargo, external and emergency lighting)
    * water installation (waste water, fresh water and toilet vacuum system; excluding the water itself)
    * liquid cooling (generation, distribution and branches)
    
    The furnishings masses exclude fittings on which they are fixed but include 
    the bolts that are used for fixing the furnishings.
    
    The mass definition between the Airbus accounting and the DIN 9020 
    (which is normally used within LTH) differs in detail. The furnishings weight 
    of the Fokker F100 is ~2% lower according to the DIN 9020 definition than according to the Airbus definition.
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFurn, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the furnishings mass
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.075) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
                
        dfus = self.parent.dfus.getValue()
        lfus = self.parent.lfus.getValue()

        return self.setValueCalc(200 + 3.35 * (lfus * dfus) ** 1.3368)

    def calcDorbathPraktikum(self):
        '''
        Calculates the furnishings mass
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 148
        '''
        dfus = self.parent.dfus.getValue()
        lfus = self.parent.lfus.getValue()
        paxSeats = self.parent.aircraft.payload.paxSeats.getValue()

        return self.setValueCalc(
            (0.115 * paxSeats ** 2 - 7.5 * paxSeats + 1000) * (1 + (10 - (lfus / dfus)) / (lfus / dfus)))


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################