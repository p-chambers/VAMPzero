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


class nPilot(parameter):
    '''
    The number of pilots operating the aircraft.  
    
    :Unit: []
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(nPilot, self).__init__(value=value, unit='', doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the number of Pilots from the design range of the aircraft. Usually, there are two pilots. 
        If the flight is longer than 12 hours a second crew is introduced as relief crew
        
        :Source: JAR-OPS Subpart Q, Flight and Duty Time Limitations and Rest Requirements, JAR 1.1105
        '''
        nPilot = 2.

        tBlock = self.parent.tBlock.getValue()

        if tBlock >= 12:
            nPilot = 4.

        return self.setValueCalc(nPilot)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
