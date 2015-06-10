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
from cmath import pi

from VAMPzero.Handler.Parameter import parameter


class twFAR25121a(parameter):
    '''
    The thrust to weight ratio for the transition climb segment
    
    The configuration is:
     
     * Take-off Flaps extended
     * Landing Gear is down
     * Full thrust on remaining engines
     * V = VLOF
     * mTOM 
    
    :Unit: [kg/m2]
    :Wiki: http://en.wikipedia.org/wiki/Thrust-to-weight_ratio
    '''

    def __init__(self, value=0., unit='kg/m2', parent='', cpacsPath=''):
        super(twFAR25121a, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

       
    def calc(self):
        '''
        Calculates the Thrust to Weight ratio for the transition climb segment
        
        :Source: Airplane Design Part I, J. Roskam, DARCorporation, 2005, Fourth Edition, p.142
        '''

        nEngine = self.parent.engine.nEngine.getValue()
        cLTO = self.parent.cLTO.getValue()
        cD0 = self.parent.cD0.getValue()
        dCDOEI = self.parent.engine.dCDOEI.getValue()
        dCDTO = self.parent.wing.flap.dCDTO.getValue()
        dCDextendedLG = self.parent.landingGear.dCDextendedLG.getValue()
        oswald = self.parent.oswald.getValue()
        aspectRatio = self.parent.wing.aspectRatio.getValue()

        if nEngine == 2.:
            climbGradient = 0.00001 # needs to be positive
        elif nEngine == 3.:
            climbGradient = 0.3
        elif nEngine == 4.:
            climbGradient = 0.5
        elif nEngine == 0.:
            climbGradient = 0.    # this switch is necessary during early iterations
        else:
            self.log.warning('VAMPzero Sizing: Could not determine suitable number of engines for OEI sizing!')

        #as FAR 25.121 asks for v between vlof and v2, CLTO needs to be corrected
        cL = cLTO / 1.1 ** 2.
        cD = cD0 + dCDTO + dCDOEI + dCDextendedLG + cL ** 2. / (aspectRatio * pi * oswald)

        tw = nEngine / (nEngine - 1.) * (cD / cL + climbGradient)

        return self.setValueCalc(tw)