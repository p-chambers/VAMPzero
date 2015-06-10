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
from cmath import tan,pi
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingUpperPoint


class xRoot(parameter):
    '''
    The x-position of the horizontal tail leading edge, root
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        '''
        #@todo: cpacsImport taperRatio: Think about an import logic for the different wings
        wingIndex = 2
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing[2]'):
            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 1, 0, 0)

            self.setValueFix(x1)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the X position of the horizontal tail depending on the location value.
        If the location value of the engine is equal to 1, configuration is conventional.
        else it is T-tail.
        '''
        location = self.parent.location.getValue()
        if location == 1.:
            self.calc = self.calcConventional
        else:
            self.calc = self.calcTtail

    def calcConventional(self):
        '''
        Calculates the X position of the horizontal tail from the fuselage length and the root chord.

        The horizontal tail lever should be as large as possible.
        Therefore the position of the horizonal tailplane is to be positioned at the rear of the fuselage

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 111
        '''
        lfus = self.parent.aircraft.fuselage.lfus.getValue()
        cRoot = self.parent.cRoot.getValue()

        return self.setValueCalc((lfus - cRoot))

    def calcTtail(self):
        '''
        Calculates the X position of the horizontal tail from the  xTip location of VTP

        '''
        xRootVTP = self.parent.aircraft.vtp.xRoot.getValue()
        phiLEVTP = self.parent.aircraft.vtp.phiLE.getValue()
        spanVTP  = self.parent.aircraft.vtp.span.getValue()
        return self.setValueCalc((xRootVTP + spanVTP * tan(phiLEVTP * pi / 180.) ))


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################