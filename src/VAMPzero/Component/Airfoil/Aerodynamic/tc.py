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


class tc(parameter):
    '''
    The thickness to chord ratio of the airfoil. Default value is set to 0.1
    
    :Unit: [ ]
    '''

    def __init__(self, value=0.1, unit='', parent='', cpacsPath=''):
        super(tc, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                 cpacsPath=cpacsPath)

    def calc(self):
        '''
        calculates the thickness to chord ratio at wing root and tip
        
        call different calc methods depending on *root* or *tip* airfoil
        '''

        if self.parent.id.find('wing') != -1 and self.parent.position == 'root':
            return self.calcWingRootTC()

        if self.parent.id.find('wing') != -1 and self.parent.position == 'tip':
            return self.calcWingTipTC()

        if self.parent.id.find('strut') != -1:
            return self.setValueCalc(self.parent.wing.tcAVG.getValue())


    def calcWingRootTC(self):
        '''
        calculates the thickness to chord ratio of the wings root airfoil from statistics and 
        from the average thickness to chord ratio of the wing
        
        :Source: Exercise Airplane Design, D. Schmitt, TU Muenchen, 2007, p. 187
        '''
        delta = 0.8
        tcAVG = self.parent.wing.tcAVG.getValue()
        return self.setValueCalc(tcAVG * 2 / (1 + delta))

    def calcWingTipTC(self):
        '''
        calculates the thickness to chord ratio of the wings tip airfoil from statistics and 
        from the average thickness to chord ratio of the wing
        
        :Source: Exercise Airplane Design, D. Schmitt, TU Muenchen, 2007, p. 187
        '''
        delta = 0.8
        tcAVG = self.parent.wing.tcAVG.getValue()
        return self.setValueCalc(tcAVG * 2 * delta / (1 + delta))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################