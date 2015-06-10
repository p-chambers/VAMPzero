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


class costMaintenance(parameter):
    '''
    The maintenance costs per flight hour
    
    :Unit: [EU/hr]
    '''

    def __init__(self, value=0., unit='EU/hr', parent='', cpacsPath=''):
        super(costMaintenance, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                              cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the maintenance cost per flight hour

        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf          
        '''
        
        tFlight = self.parent.tFlight.getValue()                 
        nEngine = self.parent.engine.nEngine.getValue()
        oEM = self.parent.oEM.getValue()
        thrustTOISA = self.parent.engine.thrustTOISA.getValue()           
        
        # Values given in source
        
        costBurden = 2.0                                                        # Cost burden [-]
        laborRate = 50.0                                                        # Labor rate per hour [eur/hr]
        
        MC_AFMAT = 0.001 * oEM * (0.21 * tFlight + 13.7) + 57.7                 # Airframe material maintenance cost (repair and replacement)
        
        MC_AFPER = laborRate * (1 + costBurden) * ((0.655 + 0.00001 * oEM) * tFlight 
                   + 0.254 + 0.00001 * oEM)                                     # Airframe personnel maintenance cost (inspection and repair)
    
        MC_ENG = nEngine * (1.5 * 0.0001019 * thrustTOISA + 30.5 * tFlight + 10.6) # Engine total maintenance cost
        
        costMaintenance = (MC_AFMAT + MC_AFPER + MC_ENG) / tFlight              # Maintenance costs per flight hour [EU/hr]
        
        return self.setValueCalc(costMaintenance)
    
    def calcKundu(self):
        '''
        Calculates the maintenance costs per flight hour from labour and material cost for airframe and engine

        :Source: Aircraft Design, A. Kundu, 2010, p.547
        '''
        costAircraft = self.parent.costAircraftMaintenance.getValue()
        costEngine = self.parent.costEngineMaintenance.getValue()

        cost = costEngine + costAircraft

        return self.setValueCalc(cost)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======