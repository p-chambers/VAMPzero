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


class massIX(parameter):
    '''
    Mass moment of inertia along the x-axis 
	
    :Unit: 'kgm2'
    :Wiki: http://en.wikipedia.org/wiki/Moment_of_inertia
    '''

    def __init__(self, value=0., unit='kgm2', parent='', cpacsPath=''):
        super(massIX, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the engines moment of inertia in reference to x-axis from the engine's mass
		
        :Source: T.Klimmek, EngineData_Statistics.xls
        '''
        mass = self.parent.mEngine.getValue()

        return self.setValueCalc(0.00009 * mass ** 2 + 0.1118 * mass - 73.377)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
