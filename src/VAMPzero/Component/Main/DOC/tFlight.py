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


class tFlight(parameter):
    '''
    The flight time for the design mission
    
    :Unit: [h]
    '''

    def __init__(self, value=0., unit='h', parent='', cpacsPath=''):
        super(tFlight, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the flight time for the flight 
        
        '''
        timeCLIMB = self.parent.timeCLIMB.getValue()
        timeCR = self.parent.timeCR.getValue()
        timeDESCENT = self.parent.timeDESCENT.getValue()

        #Convert all times from s to hr
        timeCLIMB = timeCLIMB / 3600.
        timeCR = timeCR / 3600.
        timeDESCENT = timeDESCENT / 3600.

        return self.setValueCalc(timeCLIMB + timeCR + timeDESCENT)
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################=======