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
from cmath import pi

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class rootYLocation(parameter):
    '''
    Calculates the spanwise root location of the elevator, measured from the fuselage center line
    (note: only one elevator is considered).

    :Unit: [m]

    :Source: 
    
    :Author: Lisanne van Veen
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(rootYLocation, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                            cpacsPath=cpacsPath)

    def calc(self):
        '''
        The function is a statistical relation obtained by analyzing data of large passenger aircraft.
        The design space of this equation is: 
        
        * spanWing 34.10 - 79.80 m 
        * spanHtp 12.45 - 30.37 m
        * refAreaHtp 31 - 222.57 m2

        :Source: 
        '''

        spanWing = self.parent.htp.aircraft.wing.span.getValue()
        spanHtp = self.parent.htp.span.getValue()
        refAreaHtp = self.parent.htp.refArea.getValue()

        rootYLocationElevator = 3.5502357 + 0.01219370117 * refAreaHtp - 0.3518377426 * spanHtp \
                                - 0.000286888007 * spanWing * refAreaHtp + 0.01139109091 * (spanHtp ** 2)

        return self.setValueCalc(rootYLocationElevator)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################