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


class wetArea(parameter):
    '''
    The wetted area of the wing.
    
    :Unit: [m2]
    :Wiki: http://adg.stanford.edu/aa241/drag/wettedarea.html
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(wetArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the wetted area of a wing like surface from the exposed area and the and the airfoil's tc
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.150
        '''
        expArea = self.parent.expArea.getValue()
        tcAVG = self.parent.tcAVG.getValue()

        if tcAVG < .05:
            return self.setValueCalc(2.003 * expArea)

        elif tcAVG >= .05:
            return self.setValueCalc(expArea * (1.977 + 0.52 * tcAVG))
            ###################################################################################################
            #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
            ###################################################################################################