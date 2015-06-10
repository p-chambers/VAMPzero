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
from math import e

from VAMPzero.Handler.Parameter import parameter


class dEngine(parameter):
    '''
    The outer diameter of the engine. For simplification this also includes the nacelle. 
    
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(dEngine, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the diameter of the engine from Thrust and Mach No
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.  198, Eq. 10.6 
        '''
        Tto = self.parent.thrustTO.getValue()
        bPR = self.parent.bypassRatio.getValue()

        return self.setValueCalc(0.15 * (Tto / 1000.) ** 0.5 * e ** (0.04 * bPR))

    def calcEU(self):
        '''
        Calculates the diameter of the engine using an Eureqa regression: d=f(T(kN),BPR,OPR) error~0.16
        Data for the regression was taken from open sources on engine data like e.g. wikipedia
        
        :Author: Momchil Dimchev
        '''

        b = self.parent.bypassRatio.getValue()
        p = self.parent.OPR.getValue()
        T1 = self.parent.thrustCR.getValue()

        T = T1 / 1000

        if T == 0:
            result = 0.5
        else:
            result = (0.071617201 * (4.8039379 + b) ** 0.60019219) * (
                (1.5127819 + T + 2.503902 / (b - 4.3643341)) ** 0.40880093) - 4.8039379 / (
                         p * (1.5127819 + T + 2.503902 / (b - 4.3643341)) ** 0.59882367 + 2.4216878 * (
                                                                                                          1.5127819 + T + 2.503902 / (
                                                                                                              b - 4.3643341)) ** 0.59882367 - p * p - 2.4216878 * p - 0.00030114801 * (
                                                                                                                                                                                          p) ** 2.0460701)

        return self.setValueCalc(result)

        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
