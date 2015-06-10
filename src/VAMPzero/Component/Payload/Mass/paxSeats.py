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


class paxSeats(parameter):
    '''
    The max number of available Seats depending on the class layout
    
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(paxSeats, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the number of passengers that can be seated in the cabin
        
        :Source: Preliminary Aircraft Design Course, F. Lutsch, Airbus FPO, 2008, p. 13
        '''
        self.setDeviation(0.1093) # needs to be set by the calc method when called for later use (deviation depends on the calc method)

        rangeType = self.parent.aircraft.rangeType.getValue()
        lcabin = self.parent.aircraft.fuselage.lcabin.getValue()
        nPaxR = self.parent.aircraft.fuselage.nPaxR.getValue()
        nClasses = self.parent.aircraft.fuselage.nClasses.getValue()
        dfus = self.parent.aircraft.fuselage.dfus.getValue()

        if rangeType == 0: #shortRange
            f = 0.9
        elif rangeType == 1: #mediumRange
            f = 0.8
        elif rangeType > 1:   #longRange
            f = 0.7

        if nClasses == 2:
            g = 1.
        elif nClasses == 3:
            g = .85
        elif nClasses == 1:
            g = 1.15

        j = 1.
        if dfus > 6.2:
            j = 1.4
        elif dfus > 7.:
            j = 2.

        return self.setValueCalc(g * f * lcabin * nPaxR * j)

        ###################################################################################################

#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
