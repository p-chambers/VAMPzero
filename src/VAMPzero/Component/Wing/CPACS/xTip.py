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
from cmath import tan, pi

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class xTip(parameter):
    '''
    x position of the wings tip section 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xTip, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the value for the x Position of the tip section
        @Source: boeh_da
        @Discipline: Geometry/CPACS
        @Method: Parameter 
        '''
        span = self.parent.span.getValue()
        xRoot = self.parent.xRoot.getValue()
        phiLE = self.parent.phiLE.getValue()

        return self.setValueCalc(xRoot + span / 2. * tan(phiLE * rad))

        ###################################################################################################

#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
