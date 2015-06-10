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


class xRoot(parameter):
    '''
    The x position of the root front position in absolute coordinates 
    
    :Unit: [m]
    '''
    initial = 0.
    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Retrieves the xRoot coordinate from TIGL. It will go for the main wing. The first sections x coordinate is read at eta and chord
        equal 0.
        '''
        wingIndex = 1
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing'):
            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 1, 0, 0)

            self.setValueFix(x1)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the Wing Mean Aerodynamic Chord's x Location (tip)
        locates the wing so that CoG is at 30% MAC
        '''
        lFus = self.parent.aircraft.fuselage.lfus.getValue()
        if lFus == 0.:
            return self.setValueCalc(0.)
        elif lFus != 0. and self.initial == 0.:
            self.initial = 1.
            return self.setValueCalc(0.45 * lFus)
        else:
            posCG = self.parent.aircraft.posCoG.getValue()
            cMAC = self.parent.cMAC.getValue()
            xMAC = self.parent.xMAC.getValue()
            
            mac_margin = (posCG - xMAC) / cMAC

            if  mac_margin > 0.32: 
                return self.setValueCalc(self.getValue() + (mac_margin - 0.32) * cMAC * 0.05)
            elif mac_margin < 0.3:
                return self.setValueCalc(self.getValue() - (0.3 - mac_margin) * cMAC * 0.05)
            else:
                return self.setValueCalc(self.getValue())

###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
