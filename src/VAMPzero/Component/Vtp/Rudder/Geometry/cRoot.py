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
from cmath import pi

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class cRoot(parameter):
    '''
    Calculates the root chord of the rudder.

    :Unit: [m]

    :Source: 
    
    :Author: Lisanne van Veen
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(cRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)


    def calc(self):
        '''
        Assumes that the taper ratio of the rudder is equal to the taper ratio of the vtp 
        (cTip = taperRatioVtp*cRoot).
        The reference area of the rudder and the span of the rudder could be used to calculate
        the value of the average chord length. Due to the linear taper ratio the average chord
        length is located in the middle. (cTip + cRoot)/2 = cAVG         
        The abovementioned equations are then used to calculate cRoot en cTip. 

        :Source: 
        '''

        refAreaRudder = self.parent.refArea.getValue()
        spanRudder = self.parent.span.getValue()
        taperRatioVtp = self.parent.vtp.taperRatio.getValue()

        cAVGRudder = refAreaRudder / spanRudder
        cRootRudder = 2. * cAVGRudder / (1. + taperRatioVtp)

        return self.setValueCalc(cRootRudder)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################