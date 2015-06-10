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


class lcabin(parameter):
    '''
    The length of the cabin section
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(lcabin, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the calculation method for the length of the cabin

        If lfus is fixed lcabin will be set to lfus minus nose etc
        else calcPax
        '''

        lfusStatus = self.parent.lfus.getStatus()

        if lfusStatus == 'fix':
            self.calc = self.calcLfus
        else:
            self.calc = self.calcPax


    def calcPax(self):
        '''
        Calculates the length of the cabin section from the passenger settings

        :Source: Preliminary Aircraft Design Course, F. Lutsch, Airbus FPO, 2008, p. 13
        '''
        self.setDeviation(0.2172) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
                
        paxSeats = self.parent.aircraft.payload.paxSeats.getValue()
        nPaxR = self.parent.nPaxR.getValue()
        nClasses = self.parent.nClasses.getValue()
        rangeType = self.parent.aircraft.rangeType.getValue()

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
        else:
            #@todo: calc lcabin: catch classLayout
            g = 1.

        return self.setValueCalc(paxSeats * g / (f * nPaxR))

    def calcLfus(self):
        '''
        Calculates the length of the cabin from the overall length of the fuselage

        :Source: Missing Source
        '''

        lfus = self.parent.lfus.getValue()
        ltail = self.parent.ltail.getValue()
        loverlay = self.parent.loverlay.getValue()
        lcockpit = self.parent.lcockpit.getValue()

        return self.setValueCalc(lfus - lcockpit - ltail + loverlay)
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################