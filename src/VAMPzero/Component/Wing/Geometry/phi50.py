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
from cmath import pi, tan, atan

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class phi50(parameter):
    '''
    The wings sweep angle for the 50% chord line. This is simply a helper value
    
    :Unit: [deg]
    :Wiki: http://en.wikipedia.org/wiki/Swept_wing
    '''

    def __init__(self, value=0., unit='deg', parent='', cpacsPath=''):
        super(phi50, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)


    def calc(self):
        '''
        Calculates the 50% chord sweep from geometrical dimensions of a trapezoid wing
        '''

        span = self.parent.span.getValue()
        phiLE = self.parent.phiLE.getValue()
        cRoot = self.parent.cRoot.getValue()
        cTip = self.parent.cTip.getValue()

        span = span / 2.

        xRoot = cRoot * 0.5
        xTip = cTip * 0.5 + tan(phiLE * rad) * span

        d = xTip - xRoot

        return self.setValueCalc(atan(d / span) / rad)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################