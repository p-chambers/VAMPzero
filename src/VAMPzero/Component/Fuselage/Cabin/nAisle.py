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

class nAisle(parameter):
    '''
    The number of aisles in the cabin.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Wide-body_aircraft
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(nAisle, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the calculation method for the number of Aisles

        If the fuselage diameter is fixed calcDfus is chosen
        else calcPax
        '''

        dfusStatus = self.parent.dfus.getStatus()

        if dfusStatus == 'fix':
            self.calc = self.calcDfus
        else:
            self.calc = self.calcPax

    def calcDfus(self):
        '''
        Calculates the number of aisles from the diameter of the fuselage
        Fuselage Diameters taken from Airbus Summer School Slides

        :Source: Overall Aircraft Preliminary Design, Airbus Summer School, B. Trahmer, 2011
        '''

        dfus = self.parent.dfus.getValue()

        if dfus >= 0.:
            nAisle = 1

        if dfus > 5.0:
            nAisle = 2

        return self.setValueCalc(nAisle)

    def calcPax(self):
        '''
        Calculates the number of aisles from the number of passengers.
        
        :Source: adapted from DLR-LY-IL Cabin Tool, J. Fuchte, 2011
        '''
        self.setDeviation(0.1982) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
    
        paxSeats = self.parent.aircraft.payload.paxSeats.getValue()

        if paxSeats >= 0:
            nAisle = 1

        if paxSeats > 130:
            nAisle = 1

        if paxSeats > 190:
            nAisle = 2

        return self.setValueCalc(nAisle)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################