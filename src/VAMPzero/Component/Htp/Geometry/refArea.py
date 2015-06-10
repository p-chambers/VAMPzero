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
import numpy as np
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSurfaceArea


class refArea(parameter):
    '''
    The reference area of the horizontal tailplane
    
    :Unit: [m2] 
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)
        
    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        Will get the value for refArea for HTP from CPACS via TIGL functions
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

            #@todo: cpacsImport refArea: it is assumed that the htp is number 2 wing
        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing[2]'):
            area = getWingSurfaceArea(TIGLHandle, 2)

            self.setValueFix(area)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the reference area for the horizontal tail from the volume coefficient
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 111
        '''
        lHT = self.parent.lHT.getValue()
        cHT = self.parent.cHT.getValue()
        wingCMAC = self.parent.aircraft.wing.cMAC.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()
        if lHT > 1.:
            self.calc = self.calcDetail

        return self.setValueCalc(cHT * wingCMAC * wingrefArea / lHT)

    def calcDetail(self):
        '''
        Calculates the reference area for the horizontal tail from the maximum value of different sizing cases regarding the equilibrium of the moments of the A/C
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        #Getting the maximum values of the calculations of the different flight phases
        #Take Off
        refAreaTakeOff = self.parent.refAreaTakeOff.getValue()

        #Cruise
        refAreaCruise = self.parent.refAreaCruise.getValue()

        #Landing
        refAreaLanding = self.parent.refAreaLanding.getValue()

        
        #Calculates the maximum value of all calculated areas
        refArea = max(refAreaTakeOff, refAreaCruise, refAreaLanding)

        if refArea < 1.:
            refArea = 1.
        
        return self.setValueCalc(refArea)
        
###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################