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
from VAMPzero.Handler.Parameter import parameter


class posCoG(parameter):
    '''
    fuselage center of gravity location 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(posCoG, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the coordinates of the fuselage center of gravity location
        @Source: Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999,  p. 148
        @Discipline: CoG
        @Method: Parameter 
        '''

        lfus = self.parent.lfus.getValue()
        xRootFuselage = self.parent.xRoot.getValue()
        xEngine = self.parent.aircraft.engine.xEngine.getValue()
        xEngineRel = xEngine - xRootFuselage
        if xEngineRel / lfus > 0.75:
        #average value for rear fuselage mountes engines
            return self.setValueCalc(0.47 * lfus + xRootFuselage)

        elif xEngineRel / lfus <= 0.75:
            #average value for wing-mounted-turbofans
            return self.setValueCalc(0.435 * lfus + xRootFuselage)
            ###################################################################################################
            #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
            ###################################################################################################