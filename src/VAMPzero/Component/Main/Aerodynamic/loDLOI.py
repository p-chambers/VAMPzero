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
from cmath import pi, sqrt

from VAMPzero.Handler.Parameter import parameter


class loDLOI(parameter):
    '''
    The lift-over-drag ratio for loiter condition 

    In aerodynamics, the lift-to-drag ratio, or L/D 
    ratio ("ell-over-dee"), is the amount of lift generated 
    by a wing or vehicle, divided by the drag it creates by 
    moving through the air. 
    
    :Wiki: http://en.wikipedia.org/wiki/Lift-to-drag_ratio
    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(loDLOI, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the lift over drag ratio for loiter to be green dot speed
        
        :Source: Einfuehrung in die Luftfahrttechnik, R. Voit-Nitschmann, Uni Stuttgart, 2003, p. 57
        '''
        aspectRatio = self.parent.wing.aspectRatio.getValue()
        cD0 = self.parent.cD0.getValue()
        oswald = self.parent.oswald.getValue()

        return self.setValueCalc(sqrt(cD0 * pi * aspectRatio * oswald) / (2 * cD0))
