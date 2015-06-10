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


class costEngineMaintenance(parameter):
    '''
    The maintenance costs per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costEngineMaintenance, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init',
                                                    parent=parent, cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the maintenance cost per flight hour for the engine
        The calculation method stems from the QUICE project 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        tFlight = self.parent.tFlight.getValue()
        thrustTO = self.parent.engine.thrustTO.getValue()
        nEngine = self.parent.engine.nEngine.getValue()

        thrustTO = thrustTO / (9.81 * 1000.)   #conversion N to t
        cost = nEngine * (1.5 * thrustTO + 30.5 * tFlight + 10.6) / tFlight
        return self.setValueCalc(cost)

    def calcKundu(self):
        '''
        Calculates the maintenance costs per flight hour from labour and material cost for airframe and engine

        :Source: Aircraft Design, A. Kundu, 2010, p.547
        :Source: Aircraft Commerce, No 44, 2006, p.31 
        '''
        tFlight = self.parent.tFlight.getValue()
        thrustTO = self.parent.engine.thrustTO.getValue()
        nEngine = self.parent.engine.nEngine.getValue()
        OPR = self.parent.engine.OPR.getValue()
        BPR = self.parent.engine.bypassRatio.getValue()
        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()

        #=======================================================================
        # Constants 
        #=======================================================================
        R = 63. * USDexchangeEURO      # Cost of labor hour

        #=======================================================================
        # Engine labor
        # the number of compressor stages is assumed to be constant at 15
        # the number of shafts is assumed to be two
        # conversion into euro is taken into account by labor cost
        #=======================================================================
        C1 = 1.27 - 0.2 * BPR ** 0.2
        C2 = 0.4 * (OPR / 20) ** 1.3 + 0.4
        C3 = 0.032 * 15. + 0.57
        costELabor = 0.21 * R * C1 * C3 * (1 + thrustTO / (9.81 * 1000. * nEngine)) ** 0.4

        #=======================================================================
        # Engine material
        #=======================================================================
        costEMaterial = 2.56 * (1 + thrustTO / (9.81 * 1000. * nEngine)) ** 0.8 * C1 * (C2 + C3) * USDexchangeEURO

        costEngine = nEngine * (costELabor + costEMaterial) * (tFlight + 1.3) / (tFlight - 0.25)

        cost = 2.5 * costEngine #Fudge Factor from Aircraft Commerce
        return self.setValueCalc(cost)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======