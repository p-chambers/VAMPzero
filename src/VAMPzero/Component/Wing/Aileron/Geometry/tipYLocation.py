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


class tipYLocation(parameter):
    '''
    Calculates the spanwise tip location of the aileron, measured from the fuselage center line
    (note: only one aileron is considered).

    :Unit: [m]

    :Source: 
    
    :Author: Lisanne van Veen
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(tipYLocation, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
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

        tipYLocationAileron = - 2.103872236 + 0.5286847608 * spanWing + 0.00004371791524 * (refAreaWing ** 2) \
                              - 0.0007899727342 * spanWing * refAreaWing + 0.002586029039 * (spanWing ** 2)

        # if the spanwise tip location of the aileron is larger than half of the wing span
        # set the location of the spanwise tip location equal to 95% of the half wing span 
        if tipYLocationAileron > (spanWing / 2.):
            tipYLocationAileron = (spanWing / 2.) * 0.95

        return self.setValueCalc(tipYLocationAileron)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################