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
from math import pi

from VAMPzero.Handler.Parameter import parameter


class wetArea(parameter):
    '''    
    The wetted area of all engines 
	
    :Unit: [m2]
    :Wiki: http://en.wikipedia.org/wiki/Wetted_area
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(wetArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the wetted area of the engine
        
        .. todo:: 
		
           calc wetArea: Simple solution cylinder for engine
        '''
        nEngine = self.parent.nEngine.getValue()
        lEngine = self.parent.lEngine.getValue()
        dEngine = self.parent.dEngine.getValue()
        return self.setValueCalc(lEngine * dEngine * pi * nEngine)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################