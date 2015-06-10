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


class posCoG(parameter):
    '''
    The center of gravity location of the vertical tailplane in x in absolute coordinates
    
    :Unit: [kg] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(posCoG, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the coordinates of the vertical tailplane center of gravity location
        
        :Source: Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999,  p. 148
        '''
        span = self.parent.span.getValue()
        cRoot = self.parent.cRoot.getValue()
        phiLE = self.parent.phiLE.getValue()
        phiTE = self.parent.phiTE.getValue()
        xRoot = self.parent.xRoot.getValue()
        cMAC = self.parent.cMAC.getValue()
        yMAC = self.parent.yMAC.getValue()

        bCG = span * 0.55 / 2.       # Spanwise Location of the CoG
        cCG = cRoot - bCG * tan(phiLE * rad) + bCG * tan(phiTE * rad)

        #Calculate absolute Position of Wing Root from cMAC, yMAC and Pos
        xRoot = xRoot - (0.25 * cMAC + yMAC * tan(phiLE * rad))

        #Calculated the X Location of the center of Gravity
        xCG = xRoot + tan(phiTE * rad) * bCG + 0.42 * cCG

        return self.setValueCalc(xCG)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################