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

from math import pi

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class distCLIMB(parameter):
    '''
    The distance traveled in the climb segment
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(distCLIMB, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                        cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the distance for the climb segment

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''
        #T is the indice for top, b for bottom! 
        sigmaT = self.parent.atmosphere.sigmaCR.getValue()
        sigmaB = self.parent.atmosphere.sigmaFL1500.getValue()

        IAS = self.parent.IASCLIMB.getValue()
        time = self.parent.timeCLIMB.getValue()

        tasT = IAS * sigmaT
        tasB = IAS * sigmaB

        dist = time * ((tasT + tasB / 2.))

        return self.setValueCalc(dist)