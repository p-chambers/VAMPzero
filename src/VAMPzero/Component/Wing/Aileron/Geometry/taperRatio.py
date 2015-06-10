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


class taperRatio(parameter):
    '''
    Calculates the taper ratio of the aileron (note: only one aileron is considered).

    :Unit: [-]

    :Source: 
    
    :Author: Lisanne van Veen
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(taperRatio, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)


    def calc(self):
        '''
        Sets the taperRatio of the aileron equal to the average value obtained from 
        aileron data that is measured.
        In case that the wing taper ratio is higher than 0.5, this taper ratio is used for the aileron.       

        :Source: 
        '''

        taperRatioWing = self.parent.wing.taperRatio.getValue()

        if taperRatioWing < 0.5:        # lowest taper ratio value of an aileron (measured data)
            taperRatioAileron = 0.72    # average value of measured data
        else:
            taperRatioAileron = taperRatioWing

        return self.setValueCalc(taperRatioAileron)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################