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
from cmath import pi

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class xNoseGear(parameter):
    '''
    The x-position of the nose gear
    
    :Unit: [m]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(xNoseGear, self).__init__(value=value, unit='', doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        It is the average value of different aircraft types. The value is calculated by multiplying the statical quotient of 
        the x-coordinate of the landing gear and the fuselage width by the fuselage width of the considered aircraft type.  
        
        :Source: Different airfcraft types of Airbus and Boeing 
        '''  
        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        
        Ratio_xNG_dfus = 1.13    #statical value of different aircraft types
        
        
        xNG = Ratio_xNG_dfus * dfus           
        
        return self.setValueCalc(xNG)
###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################