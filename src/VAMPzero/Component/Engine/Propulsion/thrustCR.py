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


class thrustCR(parameter):
    '''
    Thrust per engine at the beginning of the cruise segment
	
    :Unit: [N]
    '''

    def __init__(self, value=0., unit='N', parent='', cpacsPath=''):
        super(thrustCR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        calculates the cruise thrust from aircraft weight and loD for cruise condition
		
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 81
        '''
        loDCR = self.parent.aircraft.loDCR.getValue()
        nEngine = self.parent.nEngine.getValue()
        oEM = self.parent.aircraft.oEM.getValue()
        mPayload = self.parent.aircraft.payload.mPayload.getValue()
        mFuel = self.parent.aircraft.fuel.mFM.getValue()
        mFuelClimb = self.parent.aircraft.fuel.mFuelCLIMB.getValue()
        #mFuelTO     = self.parent.aircraft.fuel.mFuelTO.getValue()

        #@note: why is the last a + ?!
        TOM = oEM + mPayload + mFuel

        TWcruise = 1. / loDCR

        #estimate 0.96 as weight reduction from Takeoff to Cruise
        W = TOM * 0.96 - mFuelClimb

        #9.81 for gravity
        return self.setValueCalc(TWcruise * W * 9.81 / nEngine)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
