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
from cmath import sqrt

from VAMPzero.Handler.Parameter import parameter


class mDotEngine(parameter):
    '''
    Mass flow rate through the engine 
	
    :Unit: [kg/s]
    '''

    def __init__(self, value=0., unit='kg/s', parent='', cpacsPath=''):
        super(mDotEngine, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the mass flow ratio through one engine. 
        This calculation is based on the approximation provided by Eurequa, where the
        mass flow ratio is a function of the thrust, OPR, BPR

        :Source: Eurequa
        :Author: Momchil Dimchev, TU Delft
        '''

        T = self.parent.thrustCR.getValue()
        OPR = self.parent.OPR.getValue()
        BPR = self.parent.bypassRatio.getValue()

        T1 = T / 1000.

        return self.setValueCalc(
            1.81 * T1 + ((173. * OPR - 3990.) / (T1 - 224.)) + 3.74 * BPR * sqrt(T1) - (135. / (T1 - 266.)) - (
                4230. / (T1 - 448.)) - 50.2)
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################