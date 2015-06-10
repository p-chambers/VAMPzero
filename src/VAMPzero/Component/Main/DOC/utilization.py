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


class utilization(parameter):
    '''
    The annual utilization  defines the number of flight hours relative to the number of possible flight hours
     
    :Unit: [h/a]
    '''

    def __init__(self, value=0., unit='h/a', parent='', cpacsPath=''):
        super(utilization, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the annual flight hours
        
        The calculation method stems from the QUICE project 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        desRange = self.parent.desRange.getValue()
        tFlight = self.parent.tFlight.getValue()

        blockTimeSupplement = 1.83       #h
        annualDowntime = 2750.      #h
        hourPerAnno = 365. * 24.

        utilization = (hourPerAnno - annualDowntime) / (
            1 + desRange / (1000. * tFlight) * blockTimeSupplement / (desRange / 1000.))
        return self.setValueCalc(utilization)


    def calcLufthansa(self):
        '''
        Calculates the utilization from the number of available flight hours and 
        assuming that the aircraft is grounded for quarter of an hour. This 
        approach is taken from a Lufthansa Method quoted by W. Heinze
        
        :Source: Entwerfen von Verkehrsflugzeugen I, W. Heinze, TU Braunschweig, 2005, p. 258
        '''
        tBlock = self.parent.tBlock.getValue()

        return self.setValueCalc(4198. / (1. + 0.75 / tBlock))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################