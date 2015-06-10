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


class oswald(parameter):
    '''
    The Oswald efficiency, similar to the span efficiency, is a correction factor that represents
    the change in drag with lift of a three dimensional wing or airplane, as compared with an ideal
    wing having the same aspect ratio and an elliptical lift distribution.

    :Unit: [ ]

    :Wiki: http://en.wikipedia.org/wiki/Oswald_efficiency_number
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(oswald, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)


    def calc(self):
        '''
        This calculation takes the theorectical Oswald efficency factor of the aircraft's wing and
        applies further corrections for:
        
        * the effect of the fuselage
        * the effect of the mach number
        * the effect of viscous drag depending on the zero lift drag
        
        Within the formula presented by Nita and Scholz there is also a correction for twist distributions of the wing. 
        As these are already included in the formula for the theoretical Oswald factor these are excluded here. 
        
        :Source: Estimating the oswald factor from basic aircraft geometrical parameters, M. Nita, D. Scholz, DLRK 2012, eq. 39-42
        :Source: Drag due to Lift: Concepts for Prediction and Reduction, I. Kroo, Annual Reviews Fluid Mechanics 33, 2001, p. 587-617
        '''
        etheo = self.parent.wing.oswald.getValue()
        span = self.parent.wing.span.getValue()
        dfus = self.parent.fuselage.dfus.getValue()
        cD0 = self.parent.cD0.getValue()
        
        #=======================================================================
        # Fuselage correction
        #=======================================================================
        keF = 1 - 2 * (dfus / span) ** 2

        #=======================================================================
        #  Viscous drag correction
        #=======================================================================
        K = 0.38
        keCD0 = K * cD0

        #=======================================================================
        # Mach correction
        # Nita and Schulz apply a correction from a correlation with A320 data
        # this forumla is currently commented out as it seems to include the wave
        # drag. 
        # One Alternative seems to be a Prandtl-Glauer Correction but this 
        # also has a rather massive impact on Oswald. 
        #
        # Currently both calculations are excluded...  
        #
        #=======================================================================
        #ae          = -0.0015213
        #be          = 10.8209489
        #ce          = 1.
        #machComp    = 0.3
        #keM         = ae * (machCR/machComp-1)**be+ce

        #Prandtl- Glauert
        #keM         = sqrt(1-machCR**2)

        keM = 1.

        #=======================================================================
        # corrected Oswald Factor
        #=======================================================================
        ecorr = keM / (1 / (etheo * keF) + keCD0)

        return self.setValueCalc(ecorr)


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
