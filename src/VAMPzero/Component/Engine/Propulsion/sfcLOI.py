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


class sfcLOI(parameter):
    '''
    SFC for loiter condition 

    Specific fuel consumption, SFC, is an engineering term 
    that is used to describe the fuel efficiency of an engine 
    design with respect to thrust output. It allows the efficiency 
    of different sized engines to be directly compared.    
	
    :Unit: [kg/h/N]
    :Wiki: http://en.wikipedia.org/wiki/Thrust_specific_fuel_consumption
    '''

    def __init__(self, value=0.05, unit='kg/h/N', parent='', cpacsPath=''):
        super(sfcLOI, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        sets the value for SFC for Loiter Condition to 0.041

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition,  p.19 
        '''
        return self.setValueCalc(0.041)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################