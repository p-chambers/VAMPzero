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


class dCDTO(parameter):
    '''
    The delta Drag Coefficient for extended flaps in take-off configuration.
    
    :Unit: []
    '''
    
    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(dCDTO, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)
    
    def calc(self):                                
        '''
        Calculates the  The delta drag coefficient for extended flaps in take-off configuration. 
        Typical values for the flap deflection during take-off are 20 - 40 deg.

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1989, First Edition, p. 286

        :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        
        '''
        Aref = self.parent.refArea.getValue()
        spanInnerFlap = self.parent.spanInnerFlap.getValue()
        spanOuterFlap = self.parent.spanOuterFlap.getValue()
        spanWing = self.parent.wing.span.getValue()
        
        
        deltaFlap = 30.
  
        spanFlap = spanInnerFlap + spanOuterFlap
        
        dCDTO = 0.0023 * spanFlap/spanWing * deltaFlap
        
        return self.setValueCalc(dCDTO/Aref)  

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
