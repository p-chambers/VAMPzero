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
from math import sqrt, e

from VAMPzero.Handler.Parameter import parameter


class thrustTOISA(parameter):
    '''
    Takeoff thrust for one engine. Conditions for sea-level, standard day
    
    :Unit: [N]
	'''

    def __init__(self, value=0., unit='N', parent='', cpacsPath=''):
        super(thrustTOISA, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    #===========================================================================
    #Import 
    #===========================================================================
    def cpacsImport(self, path=''):
        '''
        .. note: 

           due to the VAMP-chain we skip this import to allow a scaling of the TWDat values
        '''
        self.setStatus('calc')
        pass

    #===========================================================================
    #Calc 
    #===========================================================================
    def calc(self):
        '''
        chooses the appropriate calculation method for the thrust at takeoff
        depending on the status of the takeoff field length
        '''
        self.calc = self.calctwTO

        #=======================================================================
        # sTOFLstatus = self.parent.aircraft.sTOFL.getStatus()
        # 
        # if sTOFLstatus == "fix":
        # else:
        #    self.calc = self.calcThrustCR
        #=======================================================================


    def calcThrustCR(self):
        '''
        Calculates the takeoff thrust backwards from the cruise thrust
        
        :Source: TU Berlin Aircraft Design Course I
        '''
        bypassRatio = self.parent.bypassRatio.getValue()
        thrustCR = self.parent.thrustCR.getValue()

        #atmosphere stuff
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        rhoCR = self.parent.aircraft.atmosphere.rhoCR.getValue()
        #        pAP             = 1.225
        #        pCR             = self.parent.aircraft.atmosphere.pCR.getValue()
        machCR = self.parent.aircraft.atmosphere.MaCR.getValue()

        rho = rhoCR / rhoAP
        p = 0.19#@todo introduce pressure ratio, should be a simple basic thing to do
        eTerm = e ** (-0.35 * machCR * p * sqrt(bypassRatio))

        D = 0.8 # maximium Cruise TU Berlin Aircraft Design Lecture I

        return self.setValueCalc(thrustCR / (D * rho * eTerm))


    def calctwTO(self):
        '''
        Calculates the takeoff thrust from the thrust to weight ratio!
        
        The thrust to weight ratios from FAR are calculated to standard atmosphere at SL and deltaT = 0.

        :Source: Uebungen im Fach Flugzeugbau, K. Kuhlmann, RWTH Aachen, 2006/2007, p. 10, eq. 30
        '''
        thrustTO = self.parent.thrustTO.getValue()

        TAP = self.parent.aircraft.atmosphere.TAP.getValue()
        pAP = self.parent.aircraft.atmosphere.pAP.getValue()

        thrustCorr = thrustTO / ( pAP / 101325.000 * (1 - 2 * (TAP - 288.15) / 288.15))

        return self.setValueCalc(thrustCorr)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################