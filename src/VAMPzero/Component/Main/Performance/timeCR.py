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

from math import pi

from VAMPzero.Handler.Parameter import parameter


class timeCR(parameter):
    '''
    The time during the cruise segment

    :Unit: [s]
    '''

    def __init__(self, value=0., unit='s', parent='', cpacsPath=''):
        super(timeCR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the time for a CruiseSegment
        depending on whether the desRange is fixed or not

        If the status of the design range is fixed calcFixRange is chosen
        else calcFixFuel is chosen
        '''
        if self.parent.desRange.getStatus() == 'fix':
            return self.calcFixRange()
        else:
            return self.calcFixFuel()

    def calcFixRange(self):
        '''
        Calculates the time for a cruise segment if the range for the segment is given

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''
        TAS = self.parent.atmosphere.TASCR.getValue()
        distCR = self.parent.distCR.getValue()
        if TAS != 0.:
            return self.setValueCalc(distCR / TAS)

    def calcFixFuel(self):
        '''
        Calculates the time for a cruise segment if the fuel for the segment is given

        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''
        #get Fuel Data
        mFuelCLIMB = self.parent.fuel.mFuelCLIMB.getValue()
        mFuelTO = self.parent.fuel.mFuelTO.getValue()
        mFuelCR = self.parent.fuel.mFuelCR.getValue()
        mFM = self.parent.fuel.mFM.getValue()

        #get Engine Data
        sfcCR = self.parent.engine.sfcCR.getValue()

        #get Mass Data
        oWE = self.parent.oEM.getValue()
        mPayload = self.parent.payload.mPayload.getValue()

        #get Atmosphere Data
        q = self.parent.atmosphere.qCR.getValue()
        TAS = self.parent.atmosphere.TASCR.getValue()

        #get Aero Data
        cD0 = self.parent.cD0.getValue()
        cDw = self.parent.wing.cDw.getValue()
        oswald = self.parent.wing.oswald.getValue()
        cDMINoffset = self.parent.wing.cDMINoffset.getValue()

        #get Wing Data
        refArea = self.parent.wing.refArea.getValue()
        aspectRatio = self.parent.wing.aspectRatio.getValue()

        #Initialize
        massCurrent = oWE + mPayload + mFM - mFuelCLIMB - mFuelTO
        fuelAvailable = mFuelCR
        timeResult = 0

        #Distance for iteration
        it = 1000

        #Fly Segments
        while fuelAvailable >= 0 and refArea != 0. and oswald != 0. and TAS != 0. and q != 0. and aspectRatio != 0. and sfcCR > 0.:
            cLCurrent = massCurrent * 9.81 / (q * refArea)
            cDCurrent = cDw + cD0 + cLCurrent * cDMINoffset + cLCurrent ** 2 / (pi * aspectRatio * oswald)
            thrustReq = cDCurrent * q * refArea
            timeSeg = it / TAS
            fuelSeg = timeSeg / 3600. * thrustReq * sfcCR #/9.81
            massCurrent = massCurrent - fuelSeg
            fuelAvailable = fuelAvailable - fuelSeg
            timeResult = timeResult + timeSeg

        return self.setValueCalc(timeResult)