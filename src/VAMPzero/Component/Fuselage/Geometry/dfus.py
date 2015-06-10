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
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getFuselagePoint, \
    getFuselageSegmentCount, getFuselageDiameter


class dfus(parameter):
    '''
    The diameter of the fuselage. The fuselage in VAMPzero has a circular shape.

    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(dfus, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        Will get the value for dfus from CPACS via TIGL functions
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/fuselages/fuselage'):
            lastSegment = getFuselageSegmentCount(TIGLHandle)

            dmax = 0.

            for i in range(lastSegment):
                diameter = getFuselageDiameter(TIGLHandle, i+1,1.)
                if diameter > dmax:
                    dmax = diameter

            self.setValueFix(dmax)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the fuselage diameter from Passenger and Cabin Data. It takes the number of passengers per row and
        the number of aisles.

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 135
        '''
        self.setDeviation(0.0687) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        nPaxR = self.parent.nPaxR.getValue()
        nAisle = self.parent.nAisle.getValue()

        return self.setValueCalc(0.56 * nPaxR + 0.5 * nAisle + 0.2)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################