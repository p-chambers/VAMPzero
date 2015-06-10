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
from cmath import sqrt

from VAMPzero.Handler.Parameter import parameter


class costNavigation(parameter):
    '''
    The navigation costs per flight hour
    
    :Unit: [EU/h]
    '''

    def __init__(self, value=0., unit='EU/h', parent='', cpacsPath=''):
        super(costNavigation, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                             cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates navigation costs per flight hour

        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                 http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf        
        '''        
        
        desRange = self.parent.desRange.getValue()                              # Design range of aircraft [m]
        mTOM = self.parent.mTOM.getValue()                                      # Maximum take-off mass [kg]
        tFlight = self.parent.tFlight.getValue()                                # Flight time of typical mission [hr]
        
        # Values given by source

        fR = 1.0                                                                # Range dependent ATC price factor (europe=1.0, transatlantic=0.7, far-east=0.6)           
        
        costNavigation = fR * (desRange / 1000) * sqrt((mTOM * 0.001) / 50) / tFlight                        

        return self.setValueCalc(costNavigation)
        
    def calcWeiss(self):
        '''
        Calculates the navigation cost per flight hour
        The calculation method stems from the QUICE project 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        mTOM = self.parent.mTOM.getValue()
        desRange = self.parent.desRange.getValue()
        tFlight = self.parent.tFlight.getValue()

        atcFactor = 1.
        cost = atcFactor * desRange / 1000. * sqrt(mTOM / (50. * 1000.)) / tFlight
        return self.setValueCalc(cost)


    def calcKundu(self):
        '''
        Calculates the navigation costs per flight hour
        
        :Source: Aircraft Design, A. Kundu, 2010, p.546
        :Source: Customer Guide to Charges - Version 5.1, Eurocontrol, 2011
        :Source: AirTOBS, Aircraft Technology & Operations Benchmark System, T. Schilling, S. Langhans, N. Hoelzel, 2011, p. 57
        '''
        mTOM = self.parent.mTOM.getValue()
        desRange = self.parent.desRange.getValue()
        tFlight = self.parent.tFlight.getValue()
        USDexchangeEURO = self.parent.USDexchangeEURO.getValue()


        #desRange is in m it needs to be converted to nm 
        distanceFactor = desRange / (1.852 * 1000. * 100.)
        weightFactor = sqrt(mTOM / (1000. * 50.))
        unitRate = 128.5 #US$/nm
        cost = distanceFactor * weightFactor * unitRate / tFlight

        return self.setValueCalc(cost)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======