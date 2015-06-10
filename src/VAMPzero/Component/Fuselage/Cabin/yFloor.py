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
from cmath import sqrt

from VAMPzero.Handler.Parameter import parameter


class yFloor(parameter):
    '''
    The width of the cabin floor. The floor is located at a 
    position zFloor beneath the widest section of the cabin
    
    :Unit:[m]     
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(yFloor, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the width of the cabin floor from the assumption of a circle 
        '''
        dcabin = self.parent.dcabin.getValue()
        zFloor = self.parent.zFloor.getValue()

        yFloor = 2. * sqrt((dcabin / 2.) ** 2 - zFloor ** 2)

        return self.setValueCalc(yFloor)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################