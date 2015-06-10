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


class nPaxR(parameter):
    '''
    The number of pax abreast in one row
    
    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(nPaxR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the calculation method for the number of seats abreast

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
        Calculates the number of passengers abreast from the fuselage diameter

        :Source: Aircraft Characteristic for Airport Planing, Airbus, Boeing, Tupolew
        '''
        dfus = self.parent.dfus.getValue()

        if dfus >= 0.:
            nPaxR = 1

        #IAI 1124A
        if dfus > 1.5:
            nPaxR = 2

        #EMB-145
        if dfus > 2.28:
            nPaxR = 3

        #TU-134
        if dfus > 2.9:
            nPaxR = 4

        #Boeing 717
        if dfus > 3.35:
            nPaxR = 5

        #Boeing 737,757
        if dfus > 3.76:
            nPaxR = 6

        #Boeing 737,757
        if dfus > 3.76:
            nPaxR = 6

        #Boeing 767
        if dfus > 5.40:
            nPaxR = 7

        #Airbus 340,330
        if dfus > 5.64:
            nPaxR = 8

        #Boeing 777
        if dfus > 6.20:
            nPaxR = 9

        #Boeing 747
        if dfus > 6.50:
            nPaxR = 10

        return self.setValueCalc(nPaxR)


    def calcPax(self):
        '''
        Calculates the number of passengers abreast in one row from the total number of passengers in the aircraft.
        
        :Source: adapted from DLR-LY-IL Cabin Tool, J. Fuchte, 2011
        '''
        self.setDeviation(0.153) # needs to be set by the calc method when called for later use (deviation depends on the calc method)        
        
        paxSeats = self.parent.aircraft.payload.paxSeats.getValue()

        if paxSeats >= 0:
            nPaxR = 5

        if paxSeats > 130:
            nPaxR = 6

        if paxSeats > 190:
            nPaxR = 7

        if paxSeats > 230:
            nPaxR = 8

        if paxSeats > 320:
            nPaxR = 9

        if paxSeats > 400:
            nPaxR = 10

        return self.setValueCalc(nPaxR)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################