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


class yRoot(parameter):
    '''
    The y position of the root leading edge of the strut.

    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(yRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the y location of the strut root leading edge according to the
        fuselage geometry.

        This calculation assumes that the strut is placed above the landing gear. The landing
        gear will extend at least as wide as the overall fuselage. Hence the strut is located at
        the outermost position of the fuselage.
        '''

        dfus = self.parent.aircraft.fuselage.dfus.getValue()

        return self.setValueCalc(dfus/2.)


###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
