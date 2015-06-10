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


class MaFL1500(parameter):
    '''
    machNumber at FL1500 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(MaFL1500, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        calculates the machnumber at FL1500
        @Source: ISA standard atmosphere
        @Discipline: Atmosphere
        @Method: Parameter 
        '''
        pass
        #        tasFL1500   = self.parent.TASFL1500.getValue()
        #        aFL1500     = self.parent.aFL1500.getValue()
        #
        #        if aFL1500 != 0.:
        #            return self.setValueCalc(tasFL1500 / aFL1500)
        #        else:
        #            self.printDivisionbyZeroError(['aFL1500'])
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################