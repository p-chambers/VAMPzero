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

class detadalpha(parameter):
    '''
    The downwash gradient describes the change in eta due to alpha.
        
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(detadalpha, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the downwash gradient to 0.45 

        .. todo:: 
        
           calc detadalpha create dependency at least to Mach
        '''
        aspectRatioWing = self.parent.aircraft.wing.aspectRatio.getValue()
        phi25Wing = self.parent.aircraft.wing.phi25.getValue()
        xMAChtp = self.parent.xMAC.getValue()
        wingxMAC25 = self.parent.aircraft.wing.xMAC25.getValue()
        span = self.parent.aircraft.wing.span.getValue()
        machCR = self.parent.aircraft.machCR.getValue()

        x = xMAChtp - wingxMAC25

        dalphaW_dalpha = 1 - (((4 + aspectRatioWing**2*(1/(cos(phi25Wing*pi/180))**2 - machCR**2))**0.5 - 2
                                    - (span**2)/(8*x**2)* (1/(cos(phi25Wing*pi/180))**2 - machCR**2))/(2 + (4
                                    + aspectRatioWing**2*(1/(cos(phi25Wing*pi/180))**2 - machCR**2))**0.5))

        return self.setValueCalc(dalphaW_dalpha)