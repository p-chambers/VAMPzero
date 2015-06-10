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


class refArea(parameter):
    '''
    Calculates the reference area of the aileron (note: only one aileron is considered).

    :Unit: [m2]

    :Source: 
    
    :Author: Lisanne van Veen
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        The function is a statistical relation obtained by analyzing data of large passenger aircraft.
        The design space of this equation is: 
        
        * refAreaWing 72.72 - 845 m2
        * spanWing 26 - 79.80 m 
    
        :Source: 
        '''

        refAreaWing = self.parent.wing.refArea.getValue()
        spanWing = self.parent.wing.span.getValue()

        refAreaAileron = 4.801831971 + 0.02990772615 * refAreaWing - 0.3615649554 * spanWing \
                         + 0.00001500935943 * (refAreaWing ** 2) - 0.0005787355345 * refAreaWing * spanWing \
                         + 0.008193522785 * (spanWing ** 2)

        return self.setValueCalc((refAreaAileron / 2.))

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
