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

from math import pi, atan, tan
from VAMPzero.Handler.Parameter import parameter

class phi50(parameter):
    '''
    The 50% chord chord sweep angle of the horizontal tail  
    
    :Unit: [deg]
    '''

    def __init__(self, value=0., unit='deg', parent='', cpacsPath=''):
        super(phi50, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the 50% chord chord sweep angle for the horizontal tailplane
        
        :Source: 
        '''
        
        phi25 = self.parent.phi25.getValue()
        aspectRatio = self.parent.aspectRatio.getValue()
        taperRatio = self.parent.taperRatio.getValue()     
        
        
        phi50 = atan(tan(phi25*pi/180) - 4/aspectRatio * (50-25)/100 * (1 - taperRatio)/(1 + taperRatio))*180/pi;

        return self.setValueCalc(phi50)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################