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
from cmath import atan, pi

from VAMPzero.Handler.Parameter import parameter


class dihedral(parameter):
    '''
    Dihedral angle is the upward angle from horizontal 
    of the wings or tailplane of a fixed-wing aircraft. 
    Anhedral angle is the name given to negative dihedral angle, 
    that is, when there is a downward angle from horizontal of the 
    wings or tailplane of a fixed-wing aircraft.
    
    :Unit: [deg]
    :Wiki: http://en.wikipedia.org/wiki/Dihedral_(aircraft)
    '''

    def __init__(self, value=0., unit='deg', parent='', cpacsPath=''):
        super(dihedral, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the dihedral of the strut from its y and z positions
        '''
        zTip  = self.parent.zTip.getValue()
        zRoot = self.parent.zRoot.getValue()
        yRoot = self.parent.yRoot.getValue()
        yTip  = self.parent.yTip.getValue()

        dz = zRoot - zTip
        dy = yRoot - yTip
        return self.setValueCalc(atan(dz/dy)*180/pi)

        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
