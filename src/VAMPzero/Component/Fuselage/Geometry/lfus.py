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
    getFuselageSegmentCount


class lfus(parameter):
    '''
    fuselage length  
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(lfus, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        Will get the value for lfus from CPACS via TIGL functions
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/fuselages/fuselage'):


            # get First Point from the Fuselage
            x1, y1, z1 = getFuselagePoint(TIGLHandle, 1, 0., 0.)

            lastSegment = getFuselageSegmentCount(TIGLHandle)
            x2, y2, z2 = getFuselagePoint(TIGLHandle, lastSegment, 1., 0.)

            self.setValueFix(x2 - x1)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the fuselage length from the other length values of the fuselage
        
        '''
        self.setDeviation(0.0014) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        ltail = self.parent.ltail.getValue()
        lcabin = self.parent.lcabin.getValue()
        loverlay = self.parent.loverlay.getValue()
        lcockpit = self.parent.lcockpit.getValue()

        return self.setValueCalc(lcockpit + lcabin + ltail - loverlay)


        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
