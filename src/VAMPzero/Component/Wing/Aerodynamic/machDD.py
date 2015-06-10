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


class machDD(parameter):
    '''
    The drag divergence Mach number indicates the speed at which the rise in 
    drag due to supersonic effects becomes significant. Within VAMPzero the 
    definition used by W.H. Mason is used where dCd/dM=0.1
    
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Drag_divergence_Mach_number
    '''


    def __init__(self, value=1., unit='', parent='', cpacsPath=''):
        super(machDD, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the drag divergence Mach number from the wings thickness to chord ratio, the wing sweep and the local Cl.
        
        :Source: W.H. Mason, Configuration Aerodynamics, 2006, p. 7-18, eq. 7-4 
        '''

        #Getters
        tcAVG = self.parent.tcAVG.getValue()
        phi25 = self.parent.phi25.getValue()
        cL = self.parent.aircraft.cLCR.getValue()

        #inverse calculation of local Cl 
        cl = cL / (1.075)

        #kA is a technology factor for determining the capabilities of the airfoil
        #Mason states 0.95 for super-critical design and 0.87 for NACA 6 series airfoils
        kA = 0.95

        phiCos = cos(phi25 * rad)
        if cl > 1.:
            self.log.warning('VAMPzero CALC: Wave Drag Convergence issues as local lift exceeds one.')
            self.log.warning('VAMPzero CALC: Will reset cl to one and continue calculation, hope to achieve convergence in the next iteration')
            cl = 1.
            machDD = kA / phiCos - tcAVG / phiCos ** 2 - cl / (10. * phiCos ** 3)
        else:
            machDD = kA / phiCos - tcAVG / phiCos ** 2 - cl / (10. * phiCos ** 3)


        return self.setValueCalc(machDD)
        
        
        
        