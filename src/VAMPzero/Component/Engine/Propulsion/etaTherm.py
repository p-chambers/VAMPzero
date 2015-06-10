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


class etaTherm(parameter):
    '''
    Thermal efficiency factor

    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Thermal_efficiency
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(etaTherm, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculation of the thermal efficiency based on TET, ambient temp, OPR, turbine and compressor efficiency.  

        :Source: J. Kurzke, Achieving maximum thermal efficiency with the simple gas turbine cycle
        :Source: Aircraft Engine Design, J. D. Mattingly, AIAA Education Series, 2002, Second Edition, p. 115
        :Author: Momchil Dimchev, TU Delft
        '''

        T = self.parent.aircraft.atmosphere.TCR.getValue()
        TET = self.parent.TET.getValue()
        OPR = self.parent.OPR.getValue()
        etaCompr = self.parent.etaCompr.getValue()
        etaTurb = self.parent.etaTurb.getValue()

        gamma = 1.4
        R = OPR ** ((gamma - 1) / gamma)

        return self.setValueCalc(
            (etaTurb * (TET / T) * (1 - 1 / R) - (R - 1) / etaCompr) / (TET / T - (R - 1) / etaCompr - 1))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################