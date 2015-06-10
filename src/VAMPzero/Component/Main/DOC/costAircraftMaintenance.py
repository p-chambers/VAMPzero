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


class costAircraftMaintenance(parameter):
    '''
    The maintenance costs per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costAircraftMaintenance, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init',
                                                      parent=parent, cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the maintenance cost per flight hour from the labor and material cost for the airframe
        The calculation method stems from the QUICE project 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        oEM = self.parent.oEM.getValue()
        tFlight = self.parent.tFlight.getValue()

        #=======================================================================
        # Airframe material cost
        #=======================================================================
        costMaterial = oEM / 1000. * (0.21 * tFlight + 13.7) + 57.5

        #=======================================================================
        # Airframe labor cost
        #=======================================================================
        laborRate = 50.       #Euro/h
        costBurden = 2
        costLabor = laborRate * (1 + costBurden) * ((0.655 + 0.01 * oEM / 1000.) * tFlight + 0.254 + 0.01 * oEM / 1000.)

        cost = (costLabor + costMaterial) / tFlight
        return self.setValueCalc(cost)

    def calcKundu(self):
        '''
        Calculates the maintenance costs per flight hour from labor and material cost for airframe 

        :Source: Aircraft Design, A. Kundu, 2010, p.547
        :Source: Aircraft Commerce, No 44, 2006, p.31
        '''

        oEM = self.parent.oEM.getValue()
        priceAC = self.parent.priceAircraft.getValue()
        tFlight = self.parent.tFlight.getValue()

        nEngine = self.parent.engine.nEngine.getValue()
        mEngine = self.parent.engine.mEngine.getValue()

        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()

        #=======================================================================
        # Constants 
        #=======================================================================
        R = 63. * USDexchangeEURO      # Cost of labor hour

        #===============================================================================
        # Airframe labor cost
        # conversion into euro is taken into account by labor cost        
        #===============================================================================
        mAirframe = (oEM - nEngine * mEngine) / 1000.
        costACLabor = (0.09 * mAirframe + 6.7 - 350. / (mAirframe + 75.)) * (
            0.8 + 0.68 * (tFlight - 0.25)) / tFlight * R

        #=======================================================================
        # Airframe material cost
        # note that this calculation is falsified by not taking into account the engine price
        # conversion to euro is taken into account by the aircraft price
        #=======================================================================
        costACMaterial = (4.2 + 2.2 * (tFlight - 0.25)) / tFlight * priceAC / 1000000.

        cost = (costACLabor + costACMaterial) * 2.5 #Fudge Factor from Aircraft Commerce
        return self.setValueCalc(cost)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======