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
import numpy as np                      #mathematical operations are possible
from numpy import unravel_index         #mathematical operations are possible (for unravel_index function)

from VAMPzero.Handler.Parameter import parameter


class posCoGMIN(parameter):
    '''
    The minimum x position of the center of gravity of the aircraft.
    It is calculated considering different combinations of fuel and payload.
    
    :Unit: [m]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(posCoGMIN, self).__init__(value=value, unit='m', doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the minimum x location for the overall center of gravity for the aircraft.
        The calculation below is based on the mass calculation in "posCoGMAX".
        It references to the massTable() from that calculation.
        '''
        #minimum value of all CoG positions (payload and fuel)
        try:
            minPosCoG = self.parent.posCoGMAX.posCoGMIN_fuel_pay0.min()
            return self.setValueCalc(minPosCoG)
        except:
            self.log.debug('VAMPzero CALC: Cannot set posMinCoG yet, probably the mass table has not been generated.')


