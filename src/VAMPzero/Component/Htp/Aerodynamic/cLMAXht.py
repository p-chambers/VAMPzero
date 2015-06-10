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
from cmath import cos, pi

class cLMAXht(parameter):
    '''
    max lift coefficient for the HTP
    
    :Unit: [ ]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cLMAXht, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the max. lift coefficient for the HTP
        
        :Source: Source: Jenkinson, Civil Jet Aircraft Design, 1999
        '''
        phi25HTP = self.parent.phi25.getValue()

        cLMAXht_2D = 1.25
        cLMAXht = 0.9 * cLMAXht_2D * cos(phi25HTP * pi/180)

        return self.setValueCalc(cLMAXht)

