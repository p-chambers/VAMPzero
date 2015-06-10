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
from cmath import pi, tan

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class aspectRatio(parameter):
    '''
    In aerodynamics, the aspect ratio of a wing is essentially the ratio of its length to its breadth (chord). 
    A high aspect ratio indicates long, narrow wings, whereas a low aspect ratio indicates short, stubby wings.
    For most wings the length of the chord is not a a constant but varies along the wing, so the aspect ratio AR 
    is defined as the square of the wingspan b divided by the area refArea of the wing planform - this is equal to 
    the length-to-breadth ratio for constant breadth.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Aspect_ratio_(wing) 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(aspectRatio, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the aspectRatio from the wings quarter-chord sweep
        depending on the status of span and refArea
        
        If the span and the reference area are fixed calcDefinition is chosen
        else calcAirbus is chosen 
        '''
        self.calc = self.calcDefinition
        if self.parent.span["status"] == 'fix' and self.parent.refArea["status"] == 'fix':
            self.calc = self.calcDefinition
        else:
            self.calc = self.calcAirbus


    def calcAirbus(self):
        '''
        Calculates the aspectRatio from the wings quarterchord sweep
        High aspectRatio and high sweep can lead to tip stall
        
        :Source: Entwurfskolloquium, T. Engelbrecht, Airbus FPO, 2009, p. 8
        :Source: changed values via Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999,  database
        '''
        self.setDeviation(0.1599) # needs to be set by the calc method when called for later use (deviation depends on the calc method)        

        phi25 = self.parent.phi25.getValue()
        
        return self.setValueCalc(4.14 / (0.86 * tan(phi25 * rad)))


    def calcDefinition(self):
        '''
        Standard definition of the aspect ratio
        '''
        span = self.parent.span.getValue()
        area = self.parent.refArea.getValue()

        return self.setValueCalc(span ** 2 / area)
         
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################