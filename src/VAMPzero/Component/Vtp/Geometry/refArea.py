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
from cmath import sqrt, pi, cos

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSurfaceArea


class refArea(parameter):
    '''
    The reference area for the vertical tail
    
    :Unit: [m2]  
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        Will get the value for refArea for VTP from CPACS via TIGL functions
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())


        #@todo: cpacsImport refArea: it is assumed that the vtp is number 3 wing
        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing[3]'):

            #get First Point from the WingRoot
            area = getWingSurfaceArea(TIGLHandle, 3)

            self.setValueFix(area / 2.)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the reference area for the vertical tail from volume coefficient
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.111 
        '''
        lVT = self.parent.lVT.getValue()
        cVT = self.parent.cVT.getValue()
        wingspan = self.parent.aircraft.wing.span.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        if lVT > 1.:
            self.calc = self.calcDetail

        return self.setValueCalc(cVT * wingspan * wingrefArea / lVT)

    def calcDetail(self):
        '''
        Calculates the reference area for the vertical tail from the maximum value of different sizing cases regarding the equilibrium of the moments of the A/C
        
        :Source: 
        '''
       
        #Getting the maximum values of the calculations of the different flight phases
        #Take Off
        refAreaTakeOff = self.parent.refAreaTakeOff.getValue()
        
        #Landing
        refAreaLanding = self.parent.refAreaLanding.getValue()
        
        
        #Calculates the maximum value of all calculated areas
        refArea = max(refAreaTakeOff, refAreaLanding)

        if refArea < 1.:
            refArea = 1.
        
        return self.setValueCalc(refArea)        
