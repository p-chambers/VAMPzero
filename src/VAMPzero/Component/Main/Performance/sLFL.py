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


class sLFL(parameter):
    '''
    The landing field length
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(sLFL, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the landing field length from the wing loading and the maximum lift at landing. 
        All calculations are on sea level
        
        :Source: Airplane Design Part I, J. Roskam, DARCorporation, 2005, Fourth Edition, p.111, eq. 3.15-3.16
        '''
        wsL = self.parent.wsL.getValue()
        cLL = self.parent.cLL.getValue()
        rhoAP = self.parent.atmosphere.rhoAP.getValue()

        #Stall speed Calculation
        Vs = sqrt(2 * wsL * 9.81 / (rhoAP * cLL)) #Eq. 3.1 from Roskam I p-90

        #Approach Speed Calculation
        Va = 1.3 * Vs * 3.6
        self.parent.vAPPR = parameter(Va, name='vAPPR', parent=self.parent)
        #make the Roskam Assumption
        #Roskam assumes ft and kts
        #kts to m is 1,8**2
        return self.setValueCalc(0.3048 * 0.3 * 0.539956803 ** 2 * Va ** 2)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################