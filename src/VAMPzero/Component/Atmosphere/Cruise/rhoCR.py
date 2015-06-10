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


class rhoCR(parameter):
    '''
    density 
    '''

    def __init__(self, value=0., unit='kg/m3', parent='', cpacsPath=''):
        super(rhoCR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates Standard Atmosphere
        @Discipline: Atmosphere
        '''

        hCR = self.parent.hCR.getValue()
        HA = self.parent.HA
        gammaH = self.parent.gammaH
        TA = self.parent.TA
        g = self.parent.g
        R_s = self.parent.R_s
        rhoA = self.parent.rhoA

        if hCR < 11000:
            rho = rhoA[0] * pow((1 + gammaH[0] / TA[0] * (hCR - HA[0])), -1 * g / (R_s * gammaH[0]) - 1)
        elif hCR > 20000:
            rho = rhoA[2] * pow((1 + gammaH[2] / TA[2] * (hCR - HA[2])), -1 * g / (R_s * gammaH[2]) - 1)
        else:
            rho = rhoA[1] * e ** (-1 * g / R_s * ((hCR - HA[1]) / TA[1]))

        return self.setValueCalc(rho)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################