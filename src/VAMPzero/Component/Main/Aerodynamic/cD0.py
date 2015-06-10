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


class cD0(parameter):
    '''
    In aerodynamics, the zero-lift drag coefficient CD0 is 
    a dimensionless parameter which relates an aircraft's 
    zero-lift drag force to its size, speed, and flying altitude.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Zero-lift_drag_coefficient 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cD0, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        calculates the zero-lift drag of the airplane from the components drag
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 281 
        '''

        Aref = self.parent.wing.refArea.getValue()

        #get the components Drag from the components
        CD0w = self.parent.wing.cD0c.getValue()
        CD0h = self.parent.htp.cD0c.getValue()
        CD0v = self.parent.vtp.cD0c.getValue()
        CD0f = self.parent.fuselage.cD0c.getValue()
        CD0e = self.parent.engine.cD0c.getValue()
        CD0s = self.parent.strut.cD0c.getValue()

        CD0c = CD0w + CD0h + CD0v + CD0f + CD0e + CD0s

        return self.setValueCalc(CD0c / Aref)
