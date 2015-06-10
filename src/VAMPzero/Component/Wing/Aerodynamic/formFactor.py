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


class formFactor(parameter):
    '''
    The form factor for the wing
    
    The parasite drag associated with skin friction and pressure drag is determined 
    by incrementing the flat plate results by a factor, to account for 
    pressure drag and the higher-than-freestream surface velocities:

    :Unit: [ ]
    :Wiki: http://adg.stanford.edu/aa241/drag/formfactor.html     
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(formFactor, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the form factor for the wing
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.283
        '''
        machCR = self.parent.aircraft.machCR.getValue()
        tcAVG = self.parent.tcAVG.getValue()
        ctm = self.parent.airfoilr.ctm.getValue()
        phi25 = self.parent.phi25.getValue()


        #@note: Root Airfoil value is taken for Calculation of the FormFaktor
        term1 = 1 + 0.6 / ctm * tcAVG + 100 * tcAVG ** 4

        #Assumption that phiMax equals phi25
        #@todo: calc formFactor:  kill assumption that phiMax equals phi25
        term2 = 1.34 * machCR ** 0.18 * (cos(phi25 * rad)) ** 0.28

        return self.setValueCalc(term1 * term2)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################