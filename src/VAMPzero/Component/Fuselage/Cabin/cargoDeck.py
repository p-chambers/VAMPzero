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

class cargoDeck(parameter):
    '''
    The layout for the cargo deck. 
    
    This is a parameter that will be exported to generate more detailed cabin layouts using the cabin design tool from J. Fuchte, DLR-LY-IL 
    
    :Unit: [ ]  
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cargoDeck, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                        cpacsPath=cpacsPath)

    def calc(self):
        '''
        Defines the layout for the cargo section. Possible outputs are:
        
        * none
        * bulk
        * A320like
        * A330like

        :Source: adapted from DLR-LY-IL Cabin Tool, J. Fuchte, 2011
        '''
        paxSeats = self.parent.aircraft.payload.paxSeats.getValue()
        rangeType = self.parent.aircraft.rangeType.getValue()

        if paxSeats == 0:
            result = 'none'
        elif rangeType == 0:
            result = 'bulk'
        elif rangeType == 1:
            result = 'A320like'
        elif rangeType > 1:
            result = 'A330like'

        return self.setValueCalc(result)


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
