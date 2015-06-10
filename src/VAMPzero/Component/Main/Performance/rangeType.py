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


class rangeType(parameter):
    '''
    The range type for the aircraft separating between
    
    * 0 = shortRange
    * 1 = mediumRange
    * 2 = longRange
    * 3 = verylongRange 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(rangeType, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                        cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the rangeType for the aircraft
        
        :Source: Preliminary Aircraft Design Course, F. Lutsch, Airbus FPO, 2008, p. 4 
        '''
        desRange = self.parent.desRange.getValue()

        if desRange < 5550000:
            switch = 0
        elif desRange < 8325000:
            switch = 1
        elif desRange < 13875000:
            switch = 2
        elif desRange > 13875000:
            switch = 3

        return self.setValueCalc(switch)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################