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
from math import pi

from VAMPzero.Handler.Parameter import parameter


class cDL(parameter):
    '''
    Drag coefficient for take off condition

    In fluid dynamics, the drag coefficient
    is a dimensionless quantity that is used
    to quantify the drag or resistance of an
    object in a fluid environment such as air or water.
    It is used in the drag equation, where a lower drag
    coefficient indicates the object will have less aerodynamic
    or hydrodynamic drag. The drag coefficient is always
    associated with a particular surface area

    :Wiki: http://en.wikipedia.org/wiki/Drag_coefficient
    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cDL, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the drag coefficient for landing condition with consideration of the increase of the HTP zero-lift 
        drag from T-strips/ L-Strips.

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 263
        '''
        AR = self.parent.wing.aspectRatio.getValue()
        Oswald = self.parent.oswald.getValue()
        cD0 = self.parent.cD0.getValue()
        dCDL = self.parent.wing.flap.dCDL.getValue()
        cDMINoffset = self.parent.wing.cDMINoffset.getValue()
        cLL = self.parent.cLL.getValue()
        dCDextendedLG = self.parent.landingGear.dCDextendedLG.getValue()

        cDL = cD0 + dCDL + cLL * cDMINoffset + cLL ** 2 / (pi * AR * Oswald) + dCDextendedLG

        return self.setValueCalc(cDL)
