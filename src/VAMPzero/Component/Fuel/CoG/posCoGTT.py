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
import cmath
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.Utilities.geom import calc_trapezoidCenterOfArea, calc_chord


class posCoGTT(parameter):
    '''
    X Position of the center of gravity of the trim tank
	
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(posCoGTT, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the posCoG of the trim tank.
        The cog of the fuel tank will be assumed to be constant for all filling levels.
        '''
        xRoot = self.parent.aircraft.htp.xRoot.getValue()
        cRoot = self.parent.aircraft.htp.cRoot.getValue()
        sweep = self.parent.aircraft.htp.phiLE.getValue()
        tr = self.parent.aircraft.htp.taperRatio.getValue()
        halfSpan = self.parent.aircraft.htp.span.getValue() / 2.
        cTip = calc_chord(cRoot, halfSpan, tr, halfSpan)
        xTip = xRoot + cmath.tan(sweep * cmath.pi / 180.) * halfSpan
        cogTrimTank = calc_trapezoidCenterOfArea(xRoot, 0.0, cRoot, xTip, cTip, halfSpan)

        return self.setValueCalc(cogTrimTank[0])


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################