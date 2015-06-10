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
from cmath import log

from VAMPzero.Handler.Parameter import parameter


class bypassRatio(parameter):
    '''
    Bypass ratio of the engine 
	
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Bypass_ratio
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(bypassRatio, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        Within this calculation the bypass ratio of the engine is determined from the engine diameter and the 
        takeoff thurst of the engine. It is questionable whether this is a suitable approach as it probably breaks with the underlying statistic.  
		
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.  198, Eq. 10.6
        '''
        Tto = self.parent.thrustTO.getValue()
        d = self.parent.dEngine.getValue()

        return self.setValueCalc(0.25 * (log(d / Tto) + 5.351))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################