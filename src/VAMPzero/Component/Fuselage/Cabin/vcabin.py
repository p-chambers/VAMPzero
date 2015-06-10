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
from cmath import atan, pi

from VAMPzero.Handler.Parameter import parameter


class vcabin(parameter):
    '''
    The volume of the cabin
    
    :Unit: [m3] 
    '''

    def __init__(self, value=0., unit='m3', parent='', cpacsPath=''):
        super(vcabin, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the volume of the cabin under the assumption of a constant cross section
        
        :Source: Productivity Metrics for Business and Regional Aircraft, Isikveren, A. T.,Goritschnig, G., Noel, M., SAE International, 2003, eq 3.2-3.4
        '''
        #=======================================================================
        # Imports
        #=======================================================================
        hs = self.parent.zFloor.getValue()
        hcabin = self.parent.hcabin.getValue()
        wcabin = self.parent.dcabin.getValue()
        wfloor = self.parent.yFloor.getValue()
        lcabin = self.parent.lcabin.getValue()

        #=======================================================================
        # Calculation
        #=======================================================================
        sigma = atan(2. * hs / wfloor)
        vcabin = lcabin / 4. * (wcabin * (pi * hcabin - sigma * wcabin) + hs * (2 * wfloor - pi * wcabin))

        return self.setValueCalc(vcabin)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################