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


class twTOP25(parameter):
    '''
    The thrust to weight ratio for take-off due to FAR takeoff field length sizing
    
    :Unit: [kg/m2]
    :Wiki: http://en.wikipedia.org/wiki/Thrust-to-weight_ratio
    '''

    def __init__(self, value=0., unit='kg/m2', parent='', cpacsPath=''):
        super(twTOP25, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the thrust to weight ratio for take-off
        
        :Source: Airplane Design Part I, J. Roskam, DARCorporation, 2005, Fourth Edition, p. 101
        '''
        #Correlation Faktor from Roskam
        #corr        = 37.5 corrected by unit conversions
        corr = 2.34

        pAP = self.parent.atmosphere.pAP.getValue()
        delta = pAP / self.parent.atmosphere.pA[0]

        sTOFL = self.parent.sTOFL.getValue()
        CLto = self.parent.cLTO.getValue()
        WSto = self.parent.wsTO.getValue()
        return self.setValueCalc(corr * WSto / (delta * CLto * sTOFL))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################