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
from cmath import sqrt

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSegmentCount, \
    getWingUpperPoint
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement


class span(parameter):
    '''
    The wingspan (or just span) of an airplane , is the distance from one wingtip to the other wingtip.
    
    :Unit: [m]
    :Wiki: http://en.wikipedia.org/wiki/Wingspan 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(span, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        Will get the value for wingSpan from CPACS via TIGL functions
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing'):

            #get First Point from the WingRoot
            wingIndex = 1

            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 1, 0, 0)

            lastSegment = getWingSegmentCount(TIGLHandle, wingIndex)
            x2, y2, z2 = getWingUpperPoint(TIGLHandle, wingIndex, lastSegment, 1, 0)
            #todo: cpacsImport span: prototype version taking leading Edge Points

            self.setValueFix((y2 - y1) * 2.)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the wingspan from reference area and aspect ratio
        '''
        self.setDeviation(0.0) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        aspectRatio = self.parent.aspectRatio.getValue()
        refArea = self.parent.refArea.getValue()

        return self.setValueCalc(sqrt(aspectRatio * refArea))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################