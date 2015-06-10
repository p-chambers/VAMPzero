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


class mFuelTO(parameter):
    '''
    The fuel used during take-off
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mFuelTO, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the fuel mass for take-off calculated from 2min full thrust at take-off
        
        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        
        .. todo::
        
           The SFC for take-off is currently only estimated as a parameter is still missing 
        '''
        thrustTO = self.parent.aircraft.engine.thrustTO.getValue()
        #todo: sfc for takeoff urgently needed
        sfc = self.parent.aircraft.engine.sfcCR.getValue()

        #takeoff time is 2 min
        time = 120.

        result = thrustTO * time / 3600. * sfc#/9.81
        return self.setValueCalc(result)
        
        
        
        
        