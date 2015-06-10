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
    The wing's center of gravity location in absolute coordinates
    
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(posCoG, self).__init__(value=value, unit='m', doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the coordinates of the wings center of gravity location
        Calculation Formula for a swept wing is taken
        
        *Frontspar will be estimated to be at 25% of the chord 
        *Rearspar will be estimated to be at 70% of the chord
        
        :Source: Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999, p. 148
        '''
        b = self.parent.span.getValue()
        cRoot = self.parent.cRoot.getValue()
        phiLE = self.parent.phiLE.getValue()
        phiTE = self.parent.phiTE.getValue()
        xMAC = self.parent.xMAC.getValue()
        yMAC = self.parent.yMAC.getValue()

        bCG = b * 0.35 / 2.       #Spanwise Location of the CoG
        cCG = cRoot - bCG * tan(phiLE * rad) + bCG * tan(phiTE * rad)

        #Calculate absolute Position of Wing Root from cMAC, yMAC and Pos
        # take the x position of the MAC
        # add the x distance to the chord of the cog 'tan(phiLE * rad) * (bCG - yMAC)'
        # add the distance to the front spar point '(0.25 * cCG)'
        # the center of gravity is at 70% of the distance between the front (0.25) and rear (0.7) spar '0.7 * (0.7 - 0.25) * cCG'
        xCG = xMAC + tan(phiLE * rad) * (bCG - yMAC) + 0.25 * cCG + (0.7 - 0.25) * cCG * 0.7 

        return self.setValueCalc(xCG)
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################