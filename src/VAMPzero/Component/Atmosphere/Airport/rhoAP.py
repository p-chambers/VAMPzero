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


class rhoAP(parameter):
    '''
    density at airport height 
    '''

    def __init__(self, value=0., unit='kg/m3', parent='', cpacsPath=''):
        super(rhoAP, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates Standard Atmosphere
        @Discipline: Atmosphere
        '''
        hAP = self.parent.hAP.getValue()
        TA = self.parent.TA
        deltaT = self.parent.deltaT.getValue()
        HA = self.parent.HA
        gammaH = self.parent.gammaH
        rhoA = self.parent.rhoA
        g = self.parent.g
        R_s = self.parent.R_s

        rho = rhoA[0] * (1 + gammaH[0] / TA[0] * (hAP - HA[0])) ** (-1. * g / (R_s * gammaH[0]) - 1.)

        rhoDeltaT = rho / (1. + deltaT / TA[0])
        return self.setValueCalc(rhoDeltaT)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################