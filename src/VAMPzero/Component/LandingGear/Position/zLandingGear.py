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
from cmath import pi, tan

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class zLandingGear(parameter):
    '''
    The z-position of the landing gear
    
    :Unit: [m]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(zLandingGear, self).__init__(value=value, unit='', doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the z-position of the landing gear with respekt to the required lift off angle (LoA) for a rotation without tail strike.
        This angle is estimated by a value of 12.5 degrees.
        '''    
        ltail = self.parent.aircraft.fuselage.ltail.getValue()
        lfus = self.parent.aircraft.fuselage.lfus.getValue()
        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        xLG = self.parent.xLandingGear.getValue()
        
        LoA = 13.5  #[deg],assumption
        
        zLG = dfus/2 + (lfus - ltail - xLG) * tan(LoA*rad)
    
        return self.setValueCalc(zLG)
###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################