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


class inflation(parameter):
    '''
    The inflation matrix used for the calculation of the direct operating costs
    
    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(inflation, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                        cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the inflation to be used in DOC - returns the price 
        escalation from an origin to a target year
        
        :Source: adapted from DLR-LY-IL DOC Tool, S. Langhans, 2010
        :Author: Momchil Dimchev
        '''
        # Constants
        year_origin = 2001
        year_target = 2011

        # Calculation
        for i in range(2):
            if i == 0:
                year = year_origin
            else:
                year = year_target

            m3 = (150. - 141.) / (1994. - 1992.)
            t3 = 141.
            x3 = 1992.
            CPI = m3 * (year - x3) + t3

            if i == 0:
                CPI_origin = CPI
            else:
                CPI_target = CPI

        return self.setValueCalc(CPI_target / CPI_origin)

        ###################################################################################################

#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
