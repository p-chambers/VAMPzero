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


class etaStrut(parameter):
    '''
    the eta coordinate of the strut tip location where eta is a nondimensional representation
    of the wing span. 0 eguals the wing root, 1 the wing tip

    :unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(etaStrut, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the strut tip to 0.65
        '''

        return self.setValueCalc(0.65)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################