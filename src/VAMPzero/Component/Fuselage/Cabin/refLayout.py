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


class refLayout(parameter):
    '''
    The reference layout for the design mission of this aircraft. 
    
    This is a combination of the class layout and the range of the aircraft. 
    This is a parameter that will be exported 
    to generate more detailed cabin layouts using the cabin design tool 
    from J. Fuchte, DLR-LY-IL
    
    :Unit: []
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(refLayout, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                        cpacsPath=cpacsPath)

    def calc(self):
        '''
        Defines the critical layout for the cabin design from the rangeType and the number of classes.
        Possible out puts are combinations of the number of classes (1,2,3) and short, medium and long range.
        
        :Source: adapted from DLR-LY-IL Cabin Tool, J. Fuchte, 2011
        '''
        rangeType = self.parent.aircraft.rangeType.getValue()
        nClasses = self.parent.nClasses.getValue()

        if rangeType == 0:
            rPart = 'SR'
        elif rangeType == 1:
            rPart = 'MR'
        elif rangeType > 1:
            rPart = 'LR'

        result = str(int(nClasses)) + 'cl_' + rPart

        return self.setValueCalc(result)
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################