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
from cmath import cos, pi

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class tcAVG(parameter):
    '''
    The average thickness to chord ratio of the wing
    
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(tcAVG, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        If the thicknesses for root and tip are fixed calcAirfoil is chosen
        else calcSweep is chosen
        '''
        if self.parent.airfoilt.tc.getStatus() == 'fix' and self.parent.airfoilr.tc.getStatus() == 'fix':
            self.calc = self.calcAirfoil

        else:
            self.calc = self.calcSweep

    def calcAirfoil(self):
        '''
        Calculates the average thickness from the airfoils thicknesses
        
        :Source: Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999,  p. 117 
        '''
        tcTIP = self.parent.airfoilt.tc.getValue()
        tcROOT = self.parent.airfoilr.tc.getValue()
        return self.setValueCalc((3. * tcTIP + tcROOT) / 4.)


    def calcSweep(self):
        '''
        Calculates the average thickness from the sweep angle 
        
        :Source: Exercise Airplane Design, D. Schmitt, TU Muenchen, 2007, p.178
        
        .. todo:: 
        
           calc tcAVG: find the factor from diagram by Schmitt on p. 180
        '''
        self.setDeviation(0.2847) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        phi25 = self.parent.phi25.getValue()

        faktor = 0.114

        return self.setValueCalc(faktor / cos(phi25 * rad))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################