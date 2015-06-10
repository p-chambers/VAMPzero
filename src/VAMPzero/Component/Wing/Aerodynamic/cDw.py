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


class cDw(parameter):
    '''
    The wave drag is the drag originating from shock waves on the wing due to sonic speeds of the freestream
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Wave_drag
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cDw, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the wings wave drag from the critical Mach number and the cruise Mach number. 
        
        Currently, this equation is producing a lot of convergence issues. Whenever the drag rise kicks in,
        massive snowballs effects evolve. We have therefor included a small lever. Wave drag is only
        included if the mach number exceeds the drag divergence mach number. 
        
        :Source: W.H. Mason, Configuration Aerodynamics, 2006, p. 7-18, eq. 7-6 
        '''

        #Getters
        machCR = self.parent.aircraft.machCR.getValue()
        machCrit = self.parent.machCrit.getValue()
        machDD = self.parent.machDD.getValue()

        if machCR >= machCrit:
            return self.setValueCalc(20. * (machCR - machCrit) ** 4.)
        else:
            return self.setValueCalc(0.0)