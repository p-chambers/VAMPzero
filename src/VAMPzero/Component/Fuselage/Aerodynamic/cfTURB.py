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
from cmath import log10

from VAMPzero.Handler.Parameter import parameter


class cfTURB(parameter):
    '''    
    Turbulent friction coefficient

    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Parasitic_drag    
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cfTURB, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the turbulent friction coefficient
        k factor was chosen for smooth paint

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.  282, Eq. 12.27-12.29
        '''
        machCR = self.parent.aircraft.machCR.getValue()
        lfus = self.parent.lfus.getValue()

        Rcut1 = 38.21 * (lfus / 0.634e-5) ** 1.053
        Rcut2 = 44.62 * (lfus / 0.634e-5) ** 1.053 * machCR ** 1.16

        Re = self.parent.reynoldsNr.getValue()
        Reapp = min([Re, Rcut1, Rcut2])

        return self.setValueCalc(0.455 / (log10(Reapp) ** 2.58 * (1 + 0.144 * machCR ** 2) ** 0.65))


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################