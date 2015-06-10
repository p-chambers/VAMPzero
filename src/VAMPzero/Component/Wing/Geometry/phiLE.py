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
from cmath import atan, pi, tan

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class phiLE(parameter):
    '''
    The angle of sweep which characterizes a swept wing is 
    conventionally measured along the 25% chord line. If 
    the 25% chord line varies in sweep angle, the leading edge is used; 
    if that varies, the sweep is expressed in sections (e.g., 25 degrees 
    from 0 to 50% span, 15 degrees from 50% to wingtip).
    
    :Unit: [deg]
    :Wiki: http://en.wikipedia.org/wiki/Swept_wing
    '''

    def __init__(self, value=0., unit='deg', parent='', cpacsPath=''):
        super(phiLE, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the leading edge sweep from quarter sweep, aspect ratio and taper ratio
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.48 
        '''
        self.setDeviation(0.0335) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        aspectRatio = self.parent.aspectRatio.getValue()
        phi25 = self.parent.phi25.getValue()
        taperRatio = self.parent.taperRatio.getValue()

        return self.setValueCalc(atan(tan(phi25 * rad) + ((1 - taperRatio) / (aspectRatio * (1 + taperRatio)))) / rad)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################