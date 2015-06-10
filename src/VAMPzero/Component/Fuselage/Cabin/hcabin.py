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


class hcabin(parameter):
    '''
    The aisle height in the cabin 
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(hcabin, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the cabin hight from the number of aisles
        
        :Source: Synthesis of Subsonic Airplance Design, E. Torenbeek, Delft University Press, 1982, p.71, fig. 3.10
        '''
        nAisle = self.parent.nAisle.getValue()

        #Standart Assumption
        hcabin = 7. * 0.3048

        if nAisle > 1.:
            hcabin = 8. * 0.3048

        return self.setValueCalc(hcabin)



        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################