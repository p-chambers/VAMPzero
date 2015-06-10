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
from math import pi, tan, sqrt

from VAMPzero.Handler.Parameter import parameter


class cLalpha(parameter):
    '''
    The rise in cL depending on alpha 
    
    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cLalpha, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)
        # set default calc method
        self.calc = self.calcVoitNitschmann

    def calc(self):
        '''
        Calculates the increase in CL depending on alpha
        '''
        pass
    
    def calcVoitNitschmann(self):
        '''
        Calculates the increase in CL depending on alpha from the aspect ratio
        
        :Source: Einfuehrung in die Luftfahrttechnik, R. Voit-Nitschmann, Uni Stuttgart, 2003, p.49 
        :Source: alternative Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.266
        '''
        AR = self.parent.aspectRatio.getValue()

        return self.setValueCalc(2 * pi * AR / (AR + 2)) # fixed formula
    
    def calcRaymerSubsonic(self):
        '''
        Calculates the increase in CL depending on alpha from the aspect ratio
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Third Edition, p.324
        '''
        AR = self.parent.aspectRatio.getValue()
        areaExp = self.parent.expArea.getValue()
        areaRef = self.parent.refArea.getValue()
        span = self.parent.span.getValue()
        phi25 = self.parent.phi25.getValue()
        dfuse = self.parent.aircraft.fuselage.dfus.getValue()
        airfoilEfficiency = 0.95
        maCr = self.parent.aircraft.machCR.getValue()
        beta_sqr = 1 - maCr**2 # is beta**2
        
        fuseLiftFactor = 1.07 * (1 + dfuse / span)
        
        num = 2 * pi * AR * areaExp / areaRef * areaExp / areaRef * fuseLiftFactor
        den = 2 + sqrt(4 + AR**2 * beta_sqr / airfoilEfficiency**2 * (1 + tan(phi25 / 180. * pi)**2 / beta_sqr))

        return self.setValueCalc(num / den)
        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################