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


class mCargo(parameter):
    '''
    The mass of additional cargo
    
    :Unit: [kg] 
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mCargo, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the mass of additional cargo from mPayload and paxSeats
        '''

        if self.parent.mPayload.getStatus() == 'fix' and self.parent.mPax.getStatus() == 'fix':
            mPayload = self.parent.mPayload.getValue()
            mPax = self.parent.mPax.getValue()

            return self.setValueCalc(mPayload - mPax)
        else:
            pass

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
