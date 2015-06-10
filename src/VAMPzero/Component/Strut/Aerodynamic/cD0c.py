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


class cD0c(parameter):
    '''
    Component zero lift drag coefficient of the wing
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Drag_coefficient
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cD0c, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the zero lift drag coefficient from the wetted area and the friction coefficients 

        For the strut we estimate a Q factor of 1.25 due to interference

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.  283
        
        .. todo: 
            
           calc CD0c: find equation for estimate laminar / turbulent transition point
        '''
        wetArea = self.parent.wetArea.getValue()
        Cflam = self.parent.cfLAM.getValue()
        Cfturb = self.parent.cfTURB.getValue()
        FF = self.parent.formFactor.getValue()
        nLam = self.parent.nLam.getValue()

        q = 1.25

        return self.setValueCalc((nLam * Cflam + (1 - nLam) * Cfturb) * FF * wetArea * q)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################