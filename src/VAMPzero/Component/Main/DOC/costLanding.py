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


class costLanding(parameter):
    '''
    The landing costs per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costLanding, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates landing costs per flight hour

        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                    http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf          
        '''
        
        mTOM = self.parent.mTOM.getValue()                                      # Maximum take-off mass [kg]
        tFlight = self.parent.tFlight.getValue()                                # Flight time per mission [hr]
        
        # Values given in source        
        
        priceLanding = 0.01                                                     # Landing fees [EU/kg]           
        
        costLanding = (priceLanding * mTOM) / tFlight
        
        return self.setValueCalc(costLanding)

    def calcQUICE(self):
        '''
        Calculates the landing costs per flight hour
        The calculation method stems from the QUICE project 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        mTOM = self.parent.mTOM.getValue()
        tFlight = self.parent.tFlight.getValue()

        landingFee = 0.0075   #landing Fee in Euro/kg

        cost = landingFee * mTOM / tFlight
        return self.setValueCalc(cost)

    def calcKundu(self):
        '''
        Calculates the landing costs per flight hour
        
        :Source: Aircraft Design, A. Kundu, 2010, p.546
        '''
        mTOM = self.parent.mTOM.getValue()
        tFlight = self.parent.tFlight.getValue()
        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()

        cost = 7.8 * mTOM * USDexchangeEURO / (1000. * tFlight)

        return self.setValueCalc(cost)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======