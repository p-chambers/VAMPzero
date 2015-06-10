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


class yEngine(parameter):
    '''
    Y-location of the engine

    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(yEngine, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the Y-location of the engine depending on the location value.
        If the location value of the engine is equal to 1, engine is wing mounted.
        else engine is fuselage mounted.

        '''
        location = self.parent.location.getValue()
        if location == 1.:
            self.calc = self.calcWingMount
        else:
            self.calc = self.calcFuselageMount

    def calcWingMount(self):
        '''
        calculates the spanwise location of the engine
        so far there is no source for a senseful estimate therefore the engine will be placed
        at 0.3 * b/2

        .. todo::

           calc yEngine: Calculation for the spanwise location of the engine, might be positioned at the kink
        '''
        wingSpan = self.parent.aircraft.wing.span.getValue()

        return self.setValueCalc(0.3 * wingSpan / 2.)



    def calcFuselageMount(self):
        '''
        Calculates the Y-location of the engine for the fuselage mounted engines from the engines diameter and the
        fuselage diameter.

        The calculation follows the picture from Stanfords online course, and taken similar to Fokker 100:

        * The pylon length between fuselage and engine is assumed to be 0.2 times of the diameter of the engine.

        :Source: http://www.fokker-aircraft.info/f100general.htm
        :Source: http://adg.stanford.edu/aa241/propulsion/engineplacement.html
        '''

        dEngine = self.parent.dEngine.getValue()
        dFuselage = self.parent.aircraft.fuselage.dfus.getValue()
        return self.setValueCalc(0.2 * dEngine + 0.5 * dEngine + dFuselage * 0.5)

        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
