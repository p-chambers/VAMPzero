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
from VAMPzero.Lib.TIGL.tigl import openTIGL, getFuselagePoint


class xRoot(parameter):
    '''
    The x position of the root front position in absolute coordinates
    
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xRoot, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Retrieves the xRoot coordinate from TIGL. It will go for the main fuselage. The first sections x coordinate is read at eta and zeta
        equal 0.
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/fuselages/fuselage'):
            self.log.debug('Importing fuselage x position...')
            try:
                # fuselage index is implicitly set to 1 in TIGL/tigl.py
                x1, _, _ = getFuselagePoint(TIGLHandle, 1, 0, 0)
            except Exception as e:
                self.log.warning(str(e))
            self.log.debug('Importing fuselage x position... {}'.format(x1))
            self.setValueFix(x1)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Sets the fuselage root x coordinate to be at 0.0
        '''
        self.setValueCalc(0.0)


        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
