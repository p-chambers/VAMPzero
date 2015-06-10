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


class nCabinCrew(parameter):
    '''
    The number of cabin crew personal for the aircraft  
    
    :Unit: []
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(nCabinCrew, self).__init__(value=value, unit='', doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the minimum number of cabin crew personal required to operate the flight. 
        For aircraft with more than 19 passengers one attendant per 50 passengers is necessary.
        
        :Source: FAA Regulations
        '''
        paxSeats = self.parent.payload.paxSeats.getValue()

        nCabinCrew = 0

        if paxSeats > 19:
            nCabinCrew = int(paxSeats / 50) + 1

        return self.setValueCalc(nCabinCrew)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
