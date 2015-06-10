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
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingUpperPoint


class zRoot(parameter):
    '''
    The z-position of the horizontal tail plane at leading edge, root
    
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
        wingIndex = 2
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing[2]'):
            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 1, 0, 0)

            self.setValueFix(z1)
            self.importSuccess()
        else:
            self.importError()


    def calc(self):
        '''
        Calculates the Z position of the horizontal tail depending on the location value.
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
        Calculates the horizontal tailplane's  z position relative to  the fuselage diameter

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 44
        '''

        dfus = self.parent.aircraft.fuselage.dfus.getValue()

        return self.setValueCalc(dfus / 4.)

    def calcTtail(self):
        '''
        Calculates the Z position of the horizontal tail from the  zTip location of VTP

        '''
        zRootVTP = self.parent.aircraft.vtp.zRoot.getValue()

        spanVTP  = self.parent.aircraft.vtp.span.getValue()

        return self.setValueCalc(zRootVTP + spanVTP)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################