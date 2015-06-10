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
from math import sqrt, pi, asin

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSegmentCount, \
    getWingUpperPoint


rad = pi / 180.


class phi25(parameter):
    '''
    The angle of sweep which characterizes a swept wing is 
    conventionally measured along the 25% chord line. If 
    the 25% chord line varies in sweep angle, the leading edge is used; 
    if that varies, the sweep is expressed in sections (e.g., 25 degrees 
    from 0 to 50% span, 15 degrees from 50% to wingtip).
    
    :Unit: [deg]
    :Wiki: http://en.wikipedia.org/wiki/Swept_wing
    '''

    def __init__(self, value=0., unit='deg', parent='', cpacsPath=''):
        super(phi25, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    #===========================================================================
    # def cpacsImport(self,path = '.\\cpacs.xml',TIXIHandle = None, TIGLHandle = None):
    #    '''
    #    Overwrites the parameters cpacsImport method!
    #    Will get the value for phi25 from CPACS via TIXI functions
    #    
    #    .. todo:: 
    #       
    #       cpacsImport phi25: Only relies on values from last positioning for the future a TIGL based approach should be coded 
    #    '''
    #    if not TIXIHandle: 
    #        TIXIHandle  = openTIXI(path)
    #    
    #    if checkElement(TIXIHandle,'/cpacs/vehicles/aircraft/model/wings/wing'):
    #        #get First Point from the WingRoot
    #        wingIndex       = 1
    #        sweep25         = getText(TIXIHandle,'/cpacs/vehicles/aircraft/model/wings/wing['+str(wingIndex)+']/positionings/positioning[last()]/sweepangle')
    #        self.setValueFix(eval(sweep25))
    #        self.importSuccess()
    #    else:
    #        self.importError()
    #===========================================================================

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Imports the quarter chord sweep angle of the wing from TIGL. It takes the wing's first and last section and reads
        y and y coordinates and from these calculates the wing sweep. 
        '''
        wingIndex = 1

        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        lastSeg = getWingSegmentCount(TIGLHandle, wingIndex)

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing'):
            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 2, 0., 0.25)
            x2, y2, z2 = getWingUpperPoint(TIGLHandle, wingIndex, lastSeg, 1., 0.25)
            #Length of the hypothenuse so we do not need atan

            h = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            self.setValueFix(asin((x2 - x1) / h) / rad)

        else:
            self.importError()


    def calc(self):
        '''
        Calculates the quarter chord sweep from the cruise mach number, the rhickness ratio and the design lift coefficient
        
        :Source: Civil Jet Aircraft Design, L.R. Jenkinson and P. Simpkin and D. Rhodes, Butterworth Heinemann, 1999, p. 116
        '''
        machCR = self.parent.aircraft.machCR.getValue()
        cLCR = self.parent.aircraft.cLCR.getValue()
        tcAVG = self.parent.tcAVG.getValue()

        if machCR > (0.1195 - 0.18 * cLCR) - 0.877 + 1.387 * tcAVG:
            phi = ((machCR - (0.1195 - 0.18 * cLCR) - 0.877 + 1.387 * tcAVG) / (0.431 * 10 ** -4)) ** 0.5

            return self.setValueCalc(phi)

            ###################################################################################################
            #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
            ###################################################################################################