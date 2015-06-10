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


class mFuelMAXinnerWT(parameter):
    '''
    The maximum fuel mass that can be stored in the inner wing tank
    
    :Unit: [kg] 
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelMAXinnerWT, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the value by certain percentage
        '''
        mFuelMAXcenterWT = self.parent.mFuelMAXcenterWT.getValue()
        mFuelMAXTT = self.parent.mFuelMAXTT.getValue()
        mFuelMAX = self.parent.mFuelMAX.getValue()
        mFuelInnerWT = 0.0
        if mFuelMAXcenterWT > 0 and mFuelMAXTT > 0:
            mFuelInnerWT = 0.6 * mFuelMAX
        elif mFuelMAXcenterWT > 0:
            mFuelInnerWT = 0.63 * mFuelMAX
        elif mFuelMAXTT > 0:
            mFuelInnerWT = 0.85 * mFuelMAX
        else:
            mFuelInnerWT = 0.92 * mFuelMAX
        self.setValueCalc(mFuelInnerWT)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################