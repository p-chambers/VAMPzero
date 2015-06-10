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
    Component zero lift drag coefficient of the fuselage
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Drag_coefficient
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cD0c, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the zero lift drag coefficient from the wetted area and the friction coefficients 
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.  281, Eq. 12.24
        
        .. todo: 
            
           calc CD0c: find equation for estimate laminar / turbulent transition point
        '''

        wetArea = self.parent.wetArea.getValue()
        cfLAM = self.parent.cfLAM.getValue()
        cfTURB = self.parent.cfTURB.getValue()
        formFactor = self.parent.formFactor.getValue()
        dragArea = self.parent.dragArea.getValue()
        nLam = self.parent.nLam.getValue()

        return self.setValueCalc((nLam * cfLAM + (1 - nLam) * cfTURB) * formFactor * wetArea + dragArea)




        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################