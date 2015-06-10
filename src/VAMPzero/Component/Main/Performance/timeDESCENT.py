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

from cmath import pi, sin, tan

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class timeDESCENT(parameter):
    '''
    The time in the descent segment
    
    :Unit: [s] 
    '''

    def __init__(self, value=0., unit='s', parent='', cpacsPath=''):
        super(timeDESCENT, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the time for the descent segment
        
        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''
        #T is the indice for top, b for bottom! 
        altT = self.parent.atmosphere.hCR.getValue()
        altB = self.parent.atmosphere.hFL1500.getValue()

        sigmaT = self.parent.atmosphere.sigmaCR.getValue()
        sigmaB = self.parent.atmosphere.sigmaFL1500.getValue()

        IAS = self.parent.IASDESCENT.getValue()
        gamma = self.parent.gammaDESCENT.getValue()

        tasT = IAS * sigmaT
        tasB = IAS * sigmaB

        if sin(gamma * rad) != 0. and (tasT + tasB / 2.) != 0.:
            time = (altT - altB) * tan((90 - gamma) * rad) / ((tasT + tasB / 2.))

            return self.setValueCalc(time)

            ###################################################################################################
            #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
            ###################################################################################################