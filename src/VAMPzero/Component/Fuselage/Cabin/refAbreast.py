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


class refAbreast(parameter):
    '''
    The reference number of pax abreast describing the layout of the cabin. 
    
    In a two-aisle aircraft with seven passengers abreast this may result in a value of 232,
    meaning that there are two passengers in the outer seatings and three in the middle  
    
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(refAbreast, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reference number of pax abreast from the number of aisles 
        and the number of passengers per Row

        :Source: adapted from DLR-LY-IL Cabin Tool, J. Fuchte, 2011
        '''
        nPaxR = self.parent.nPaxR.getValue()
        nAisles = self.parent.nAisle.getValue()

        result = ''

        if nPaxR == 5:
            result = '32'

        if nPaxR == 6:
            if nAisles == 1:
                result = '33'
            elif nAisles == 2:
                result = '222'

        if nPaxR == 7:
            if nAisles == 1:
                result = '34'
            elif nAisles == 2:
                result = '232'

        if nPaxR == 8:
            if nAisles == 1:
                result = '44'
            elif nAisles == 2:
                result = '242'

        if nPaxR == 9:
            if nAisles == 2:
                result = '252'

        if nPaxR == 10:
            if nAisles == 2:
                result = '343'

        return self.setValueCalc(result)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################