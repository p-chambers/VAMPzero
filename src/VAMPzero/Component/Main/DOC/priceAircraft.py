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
from cmath import e, log10

from VAMPzero.Handler.Parameter import parameter


class priceAircraft(parameter):
    '''
    The market price of the aircraft including engines. The market price of an aircraft is usually 
    way lower than the list price. As this price is important for the airline's cost it is included here
    
    :Unit: [EU]
    '''

    def __init__(self, value=0., unit='EU', parent='', cpacsPath=''):
        super(priceAircraft, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                            cpacsPath=cpacsPath)

    def calc(self):
        '''
        The calculation method stems from the QUICE project. It calculates the aircraft price from a fixed price per kg oEM 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        oEM = self.parent.oEM.getValue()
        priceoEM = 1370.              #EU per kg

        return self.setValueCalc(oEM * priceoEM)


    def calcPloetner(self):
        '''
        Calculates the engine price from a regression applied to the Airliner Price Guide.
        The idiosyncratic error is neglected
        
        :Source: Influence of aircraft parameters on aircraft market price, K. Ploetner, M. Cole, M. Hornung, A. Isikveren, P. Wesseler, C. Essling, DLRK, 2012, table 3  
        '''
        desRange = self.parent.desRange.getValue()
        machCR = self.parent.machCR.getValue()
        paxSeats = self.parent.payload.paxSeats.getValue()
        vcabin = self.parent.fuselage.vcabin.getValue()
        sTOFL = self.parent.sTOFL.getValue()
        USDexchange = self.parent.USDexchangeEURO.getValue()

        #=======================================================================
        # Constants
        #=======================================================================
        a0 = 0.092
        b = 0.000047
        c = 0.207
        d = 1.320
        eR = 0.00023
        f = 0.00018

        Logprice = a0 + b * desRange / 1000. + c * machCR + d * log10(paxSeats) + eR * vcabin + f * sTOFL
        price = e ** Logprice * 1000000 * USDexchange

        return self.setValueCalc(price)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======