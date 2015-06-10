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


class MaFL100(parameter):
    '''
    machNumber at FL100 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(MaFL100, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        calculates the machnumber at FL100
        @Source: ISA standard atmosphere
        @Discipline: Atmosphere
        @Method: Parameter 
        '''
        pass
        #        tasFL100   = self.parent.TASFL100.getValue()
        #        aFL100     = self.parent.aFL100.getValue()
        #
        #        if aFL100 != 0.:
        #            return self.setValueCalc(tasFL100 / aFL100)
        #        else:
        #            self.printDivisionbyZeroError(['aFL100'])
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################