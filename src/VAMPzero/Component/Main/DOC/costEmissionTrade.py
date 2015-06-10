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


class costEmissionTrade(parameter):
    '''
    The cost arising from European Emission Trading per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costEmissionTrade, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                                cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the emission cost from the EU-Emission Trading Scheme
        
        :Source: Evaluation of worldwide Noise and Pollutant Emission Cost for Integration into Direct Operating Cost Methods, A. Johanning, D. Scholz, DLRK, 2012. eq. 15-23
        :Source: Meeting Carbon Budgets the need for a step change, Committee on Climate Change (CCC), 2009, p. 17
        '''

        mBlock = self.parent.fuel.mFM.getValue()
        tFlight = self.parent.tFlight.getValue()

        #===============================================================================
        # Constants 
        #===============================================================================
        co2 = 3.15             # amount of co2 generated per kg fuel
        fiscalyear = 2012.            # year for the analysis
        pCO2freep = 0.82             # percentage of free certificates
        ctCO2m = 20.              # 20/EURO per t CO2 as projected price for 2020, see CCC p.17
        nmov2010 = 64418742.        # Number of aircraft movements in the world
        nmovEU2010 = 17596411.        # Number of aircraft movements in the EU

        #===============================================================================
        # Calculation
        #===============================================================================
        # Emission of CO2 per flight
        eCO2 = mBlock * co2 / 1000.

        # Future CO2 Emission        
        pCO2fut = 100. + 2.5 * (fiscalyear - 2005)
        # Amount of free Emissions
        pCO2free = pCO2freep / pCO2fut
        # Cost from Emission Certificates
        ctCO2 = (1 - pCO2free) * ctCO2m

        # number of aircraft movements in the world 
        nmov = nmov2010 + 4.8 / 100. * nmov2010 * (fiscalyear - 2010)
        # number of aircraft movements in the EU
        nmovEU = nmovEU2010 + 4. / 100. * nmovEU2010 * (fiscalyear - 2010)
        #percentage of movements in EU
        pmovEU = nmovEU / nmov

        cost = ctCO2 * pmovEU * eCO2 / tFlight

        return self.setValueCalc(cost)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======