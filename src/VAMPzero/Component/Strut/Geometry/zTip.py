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
from cmath import tan, pi, cos, sin

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class zTip(parameter):
    '''
    The z position of the tip leading edge of the strut.

    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(zTip, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the z location of the strut tip leading edge according to the
        wing geometry.

        The calculation places the strut tip near the front spar of the wing. Hence,
        it should benefit aerostatic and maybe aeroelastic behavior as it helps the wing
        to wash out.

        Calculation is only valid if the strut is twisted around the dihedral axis
        '''
        dihedral_wing = self.parent.aircraft.wing.dihedral.getValue()
        phi25_wing = self.parent.aircraft.wing.phi25.getValue()
        span_wing = self.parent.aircraft.wing.span.getValue()
        zRoot_wing = self.parent.aircraft.wing.zRoot.getValue()

        d_fus = self.parent.aircraft.fuselage.dfus.getValue()

        etaStrut = self.parent.etaStrut.getValue()
        dfus = self.parent.aircraft.fuselage.dfus.getValue()

        return self.setValueCalc(zRoot_wing + tan(dihedral_wing*rad) * span_wing / 2. * (etaStrut-dfus/span_wing))


###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
