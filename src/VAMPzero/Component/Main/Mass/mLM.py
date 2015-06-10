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
from math import e

from VAMPzero.Handler.Parameter import parameter


class mLM(parameter):
    '''
    The maximum landing mass for the aircraft
    
    :Unit: [kg] 
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mLM, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the maximum landing mass from the maximum take-off mass, maximum zero fuel mass and the range
        
        :Source: Synthesis of Subsonic Airplance Design, E. Torenbeek, Delft University Press, 1982, p. 275, Eq. 8-2
        '''
        self.setDeviation(0.039) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        mZFW = self.parent.mZFW.getValue()
        mTOM = self.parent.mTOM.getValue()
        Range = self.parent.desRange.getValue()

        return self.setValueCalc((0.2 + 0.9 * e ** (-Range / 1854)) * (mTOM - mZFW) + mZFW)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
