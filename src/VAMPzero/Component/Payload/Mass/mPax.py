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


class mPax(parameter):
    '''
    The mass of all passengers
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mPax, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the mass of all passengers
        '''
        self.setDeviation(0.0493) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        mSinglePax = self.parent.mSinglePax.getValue()
        paxSeats = self.parent.paxSeats.getValue()

        return self.setValueCalc(paxSeats * mSinglePax)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################