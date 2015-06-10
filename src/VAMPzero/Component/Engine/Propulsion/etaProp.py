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


class etaProp(parameter):
    '''
    Propulsive efficiency factor
	
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Propulsive_efficiency
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(etaProp, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculation of the propulsive efficiency based on TAS, thrust, mass flow rate.  

        :Source: Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999,  p. 221
        :Author: Momchil Dimchev, TU Delft
        '''

        Tcr = self.parent.thrustCR.getValue()
        TAS = self.parent.aircraft.atmosphere.TASCR.getValue()
        mDotEngine = self.parent.mDotEngine.getValue()

        return self.setValueCalc(2. * TAS / (Tcr / mDotEngine + 2. * TAS))
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################