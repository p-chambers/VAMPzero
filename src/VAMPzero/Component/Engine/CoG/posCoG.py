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


class posCoG(parameter):
    '''
    X Position of the center of gravity of the engine
	
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(posCoG, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the posCoG from the engine's x Position and the engine's length. 
        The CoG of an engine will be estimated for 0.3* engine length

        .. todo:: 

           calc posCoG: find source for engine CoG  
        '''
        xeng = self.parent.xEngine.getValue()
        leng = self.parent.lEngine.getValue()

        return self.setValueCalc(xeng + 0.3 * leng)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################