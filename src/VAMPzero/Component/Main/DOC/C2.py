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


class C2(parameter):
    '''
    Route dependent yearly costs

    :Unit: [EU/hr]     
    
    :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
            http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf
    '''
    
    def __init__(self, value=0., unit='EU/hr', parent='', cpacsPath=''):
        super(C2, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)
    
    def calc(self):
        '''
        Calculation method for yearly route dependent costs

        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf      
        '''                                  
        
        costFuel = self.parent.costFuel.getValue()                              # Fuel cost [EU/hr]
        costLanding = self.parent.costLanding.getValue()                        # Landing cost [EU/hr]
        costGround = self.parent.costGround.getValue()                          # Ground handling cost [EU/hr]
        costNavigation = self.parent.costNavigation.getValue()                  # Navigation cost [EU/hr]
        costMaintenance = self.parent.costMaintenance.getValue()                # Maintenance cost [EU/hr]
             
        # Calculations - Route dependent costs per flight hour [EU/hr]
        
        C2 = costFuel + costLanding + costGround + costNavigation + costMaintenance
        
        return self.setValueCalc(C2)
        
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################