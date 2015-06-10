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


class mFuelMAX(parameter):
    '''
    The maximum fuel mass that can be stored in the tanks
    
    :Unit: [kg] 
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelMAX, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the calc method to calcHeinze
        '''
        self.calc = self.calcHeinze


    def calcHeinze(self):
        '''
        Calculates the maximum fuel mass that can be stored in the wing from the 
        geometrical definition of a single trapezoid
        
        k Faktor from Heinze was chosen to be 0.32
        
        :Source: Entwerfen von Verkehrsflugzeugen II, W. Heinze, TU Braunschweig, 2005, pp. 169
        '''

        taperRatio = self.parent.aircraft.wing.taperRatio.getValue()
        span = self.parent.aircraft.wing.span.getValue()
        cRoot = self.parent.aircraft.wing.cRoot.getValue()
        tcRoot = self.parent.aircraft.wing.airfoilr.tc.getValue()
        tcTip = self.parent.aircraft.wing.airfoilt.tc.getValue()

        k = 0.32
        density = 775 #[kg/m3]

        #Calculate the tanks Volume
        if tcRoot != 0.:
            brace1 = 1 + taperRatio ** 2 * tcTip / tcRoot + taperRatio * sqrt(tcTip / tcRoot)
        else:
            brace1 = 0.

        Vtank = 2. / 3. * span / 2. * k * cRoot ** 2 * tcRoot * (brace1)

        #Return result as Volume of the tank times the density
        return self.setValueCalc(Vtank * density)


    def calcFLOPS(self):
        '''
        Calculation of the maximum Fuel Mass from the amount of fuel that can be stored in the wing
        Calculation Method in Flops sets FWMX to 23 as default. This is altered to 23/2.2046 for SI Units
        
        :Source: Flight Optimization System (FLOPS) User's Guide,  McCullers, L.A., NASA Langeley, 2009, p. 
        '''

        FWMX = 23 / 2.2046
        refArea = self.parent.aircraft.wing.refArea.getValue()
        taperRatio = self.parent.aircraft.wing.taperRatio.getValue()
        span = self.parent.aircraft.wing.span.getValue()
        tcAVG = self.parent.aircraft.wing.tcAVG.getValue()

        #Span and Area must be converted into ft / ft**2 for correct results
        term1 = tcAVG * (refArea / 0.092903 ) ** 2 / (span / 0.3048)
        term2 = taperRatio / (1 + taperRatio) ** 2

        FuelMass = FWMX * term1 * (1 - term2)

        return self.setValueCalc(FuelMass)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################