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
from cmath import e, log, pi

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class desRange(parameter):
    '''
    The design range for the aircraft. 
    
    This is the range that will be used together with the specified payload to size the aircraft.
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(desRange, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets the calc method to calcSum
        '''
        self.calc = self.calcSum

    def calcSum(self):
        '''
        Calculates the design range from the sum of all distances
        
        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''

        distCLIMB = self.parent.distCLIMB.getValue()
        distDESCENT = self.parent.distDESCENT.getValue()
        distCR = self.parent.distCR.getValue()
        distRES = self.parent.distRES.getValue()

        return self.setValueCalc(distCLIMB + distCR + distDESCENT + distRES)

    def calcBreguet(self):
        '''
        Calculates the values for the designRange from given airplane
        Returns zero if mFM is zero
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p.164
        '''
        TAS = self.parent.atmosphere.TASCR.getValue()
        loDCR = self.parent.loDCR.getValue()
        sfcCR = self.parent.engine.sfcCR.getValue()
        oEM = self.parent.oEM.getValue()
        mPayload = self.parent.payload.mPayload.getValue()
        mFM = self.parent.fuel.mFM.getValue()
        resTime = self.parent.timeRES.getValue()
        loDLOI = self.parent.loDLOI.getValue()
        sfcLOI = self.parent.engine.sfcLOI.getValue()

        ldw = oEM + mPayload
        tow = oEM + mPayload + mFM

        if mFM == 0.:
            return self.setValueCalc(0.)
        else:
            if sfcCR != 0. and loDLOI != 0:
                term1 = TAS * loDCR / (sfcCR / 3600.) / 1000.
                #correct landing weight for reserveTime
                bla = e ** (-resTime * sfcLOI / loDLOI)

            else:
                term1 = 0.
                tow = 0.

            if tow != 0.:
                term2 = tow / ldw * 0.951 * bla
            else:
                term2 = 1.

            return self.setValueCalc(term1 * log(term2))

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
