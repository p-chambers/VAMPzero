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


class cLMAX(parameter):
    '''
    The max lift coefficient for the clean wing
    
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cLMAX, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the max cL for the wing
        
        :Source: Airplane Design Part II, J. Roskam, DARCorporation, 2005, Fourth Edition, p.168
        '''
        Clmaxr = self.parent.airfoilr.clMAX.getValue()
        Clmaxt = self.parent.airfoilt.clMAX.getValue()

        taperRatio = self.parent.taperRatio.getValue()
        phi25 = self.parent.phi25.getValue()

        #Calc k faktor
        k = -0.117 * taperRatio + 0.997

        #Calc CLmax for unswept wing
        CLmaxunswept = k * (Clmaxr + Clmaxt) / 2.

        #Correct for swept wings
        return self.setValueCalc(CLmaxunswept * cos(phi25 * rad))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################