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


class avgChord(parameter):
    '''
    Calculates the average chord of one single spoiler.

    :Unit: [m]

    :Source: 
    
    :Author: Lisanne van Veen
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(avgChord, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        The function is a statistical relation obtained by analyzing data of large passenger aircraft.
        The design space of this equation is: 
        
        * refAreaWing 122.4 - 845 m2
        * spanWing 34.1 - 79.80 m 
    
        :Source: 
        '''

        refAreaWing = self.parent.wing.refArea.getValue()
        spanWing = self.parent.wing.span.getValue()

        avgChordSPO = 0.4154405725 + 0.001032682668 * spanWing + 0.0008910763947 * refAreaWing

        return self.setValueCalc(avgChordSPO)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
