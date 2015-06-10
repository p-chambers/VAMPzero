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
from VAMPzero.Lib.TIXI.tixi import checkElement, openTIXI
from VAMPzero.Lib.TIGL.tigl import getWingUpperPoint, openTIGL


rad = pi / 180.


class zRoot(parameter):
    '''
    The z position at wing root in absolute coordinates
    
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(zRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        '''
        #@todo: cpacsImport taperRatio: Think about an import logic for the different wings
        wingIndex = 1
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing'):
            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 1, 0, 0)

            self.setValueFix(z1)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the wing position depending on the location of the wing.

        The wing may either be high or low
        '''
        loc = self.parent.location.getValue()

        if loc:
            self.calc = self.calcLow
        else:
            self.calc = self.calcHigh


    def calcLow(self):
        '''
        Calculates the wings z position relative to thickness to chord and fuselage diameter

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 30
        '''

        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        tc = self.parent.tcAVG.getValue()
        cRoot = self.parent.cRoot.getValue()

        return self.setValueCalc((tc * cRoot / 2. - dfus / 2.))

    def calcHigh(self):
        '''
        Calculates the wings z position relative to thickness to chord and fuselage diameter

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 30
        '''

        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        tc = self.parent.tcAVG.getValue()
        cRoot = self.parent.cRoot.getValue()

        return self.setValueCalc((tc * cRoot / 2. - dfus / 2.)*-1.)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################