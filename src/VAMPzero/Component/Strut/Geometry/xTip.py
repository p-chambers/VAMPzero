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


class xTip(parameter):
    '''
    The x position of the tip leading edge of the strut.

    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xTip, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the leading edge postion of the strut tip from the wing geometry

        The calculation places the strut tip near the front spar of the wing. Hence,
        it should benefit aerostatic and maybe aeroelastic behavior as it helps the wing
        to wash out.

        :Source: Discussion at DLR-LY
        '''
        xRoot_wing = self.parent.aircraft.wing.xRoot.getValue()
        cRoot_wing = self.parent.aircraft.wing.cRoot.getValue()
        phiLE_wing = self.parent.aircraft.wing.phiLE.getValue()
        span_wing = self.parent.aircraft.wing.span.getValue()

        cRoot = self.parent.cRoot.getValue()
        etaStrut = self.parent.etaStrut.getValue()
        depth = self.parent.depth.getValue()
        dfus = self.parent.aircraft.fuselage.dfus.getValue()


        # Go to the root position of the wing.
        # Move outwards along the leading edge
        # The front spar of the wing and and front spar of the strut shall meet
        # The front spar of the wing is always located at 10% of the root chord of the wing behind the leading edge
        # The strut spar is located at 30% of the profile as this is the location of the highest thickness.
        if 0.1 * cRoot_wing < 0.3 *cRoot:
            self.log.warn('VAMPzero STRUT: The leading edge of the strut exceeds the leading edge of the wing!')
            self.log.warn('VAMPzero STRUT: Decrease strut depth or adept spar positions.')
        loc = xRoot_wing + tan(phiLE_wing*rad) * span_wing/2. * (etaStrut-dfus/span_wing) + 0.1 * cRoot_wing - 0.3 *cRoot
        return self.setValueCalc(loc)


###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
