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
from cmath import pi, cos, sin

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class xRoot(parameter):
    '''
    The x position of the root leading edge of the strut.

    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the leading edge postion of the strut root from the tip location
        of the strut.

        For the strut the calculation of the sweep angle is reverse, i.e. the tip location is
        fixed by the wing geometry. The sweep angle may be used to shift the root position. For
        the wing this used to be the other way round.

        :Source: Discussion at DLR-LY
        '''

        xTip = self.parent.xTip.getValue()
        phiLE = self.parent.phiLE.getValue()
        yTip = self.parent.yTip.getValue()
        yRoot = self.parent.yRoot.getValue()
        return self.setValueCalc(xTip - sin(phiLE*rad)*(yTip-yRoot))


###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
