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


class machCrit(parameter):
    '''
    The critical Mach number is defined as the Mach number where for 
    the first time the freestream becomes sonic at the upper surface of the wing.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Critical_Mach_number
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(machCrit, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the critical Mach number from the drag divergence Mach number.
        
        :Source: W.H. Mason, Configuration Aerodynamics, 2006, p. 7-19, eq. 7-8 
        '''
        machDD = self.parent.machDD.getValue()

        return self.setValueCalc(machDD - (0.1 / 80.) ** (1. / 3.))
        
    
    