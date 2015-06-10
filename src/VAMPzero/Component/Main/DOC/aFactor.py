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

class aFactor(parameter):
    '''
    Calculation of annuity factor
    
    :Unit: [-]
    '''
    
    def __init__(self, value=0., unit='-', parent='', cpacsPath=''):
        super(aFactor, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                              cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculation method annuity factor

        Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf       
        '''                               

        # Values presented in source
        
        IR = 0.05                                                               # Interest rate [-]
        DP = 14.0                                                               # Depreciation period [years]
        fRV = 0.1                                                               # Residual value factor [-]
        
        # Annuity factor
        
        a = IR * ((1 - fRV * (1 / (1 + IR)) ** DP) / (1 - (1 / (1 + IR)) ** DP))
        
        return self.setValueCalc(a)