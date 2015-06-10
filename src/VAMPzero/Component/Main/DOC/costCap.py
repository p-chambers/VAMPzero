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

class costCap(parameter):
    '''
    Capital costs calculated using TU Berlin method

    :Unit: [EU/hr]    
    '''
    
    def __init__(self, value=0., unit='EU/hr', parent='', cpacsPath=''):
        super(costCap, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)
    
    def calc(self):
        '''
        Calculates captical costs
        
        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf 
        '''
        
        aFactor = self.parent.aFactor.getValue()                                # Annuity factor [-]
        oEM = self.parent.oEM.getValue()                                        # Operational empty mass [kg]
        nEngine = self.parent.engine.nEngine.getValue()                         # Number of engines [#]
        mEngine = self.parent.engine.mEngine.getValue()                         # Engine mass [kg]
        tFlight = self.parent.tFlight.getValue()                                # Flight time of one flight [hr]
        flightCycles = self.parent.flightCycles.getValue()                      # Number of flight cycles per year [#]
        
        # Values presented in source         
        
        priceOEW = 1150.0                                                       # Price per kg OEW [EU/kg]
        priceEng = 2500.0                                                       # Price per Engine weight [EU/kg]
        fIns = 0.005                                                            # Insurance rate [-]
        
        # Captical cost is assumed  to be a linear function of the oEM
        
        costCap = ((priceOEW * (oEM - mEngine * nEngine) + mEngine * nEngine * priceEng) * (aFactor + fIns)) / (tFlight * flightCycles)
        
        return self.setValueCalc(costCap)
        
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
        
        