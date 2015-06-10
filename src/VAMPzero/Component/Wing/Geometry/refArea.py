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


class refArea(parameter):
    '''
    The reference area of the wing 
    
    
    :Unit: [m2]
    :Wiki: http://adg.stanford.edu/aa241/wingdesign/winggeometry.html
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reference area of the wing for given aspect ratio and span
        depending on the status of span and aspect ratio
        
        If the span and the aspect ratio are fixed calcGeom is chosen 
        else calcSizing is chosen
        '''

        if self.parent.span.getStatus() == 'fix' and self.parent.aspectRatio.getStatus() == 'fix':
            self.calc = self.calcGeom
        else:
            self.calc = self.calcSizing


    def calcGeom(self):
        '''
        Calculates the reference area of the wing for given aspectRatio and span
        '''
        span = self.parent.span.getValue()
        aspectRatio = self.parent.aspectRatio.getValue()

        return self.setValueCalc(span ** 2 / aspectRatio)

    def calcSizing(self):
        '''
        Calculates the reference area of the wing for maximum wing loading
        '''
        self.setDeviation(0.0) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        mTOM = self.parent.aircraft.mTOM.getValue()
        WSmax = self.parent.aircraft.wsMAX.getValue()

        return self.setValueCalc(mTOM / WSmax)
