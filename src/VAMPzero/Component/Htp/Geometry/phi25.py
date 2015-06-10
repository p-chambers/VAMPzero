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

from math import pi, sqrt, asin

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import checkElement, openTIXI
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingUpperPoint, \
    getWingSegmentCount


rad = pi / 180.


class phi25(parameter):
    '''
    The quarter chord sweep angle of the horizontal tail  
    
    :Unit: [deg]
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
    #    if checkElement(TIXIHandle,'/cpacs/vehicles/aircraft/model/wings/wing[2]'):
    #        #get First Point from the WingRoot
    #        wingIndex       = 2
    #        sweep25         = getText(TIXIHandle,'/cpacs/vehicles/aircraft/model/wings/wing['+str(wingIndex)+']/positionings/positioning[last()]/sweepangle')
    #        self.setValueFix(eval(sweep25))
    #        self.importSuccess()
    #    else:
    #        self.importError()    
    #===========================================================================


    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Imports the quarter chord sweep angle of the htp from TIGL. It takes the htp's first and last section and reads
        y and y coordinates and from these calculates the htp sweep. 
        '''
        wingIndex = 2

        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        lastSeg = getWingSegmentCount(TIGLHandle, wingIndex)

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing[2]'):
            x1, y1, z1 = getWingUpperPoint(TIGLHandle, wingIndex, 1, 0., 0.25)
            x2, y2, z2 = getWingUpperPoint(TIGLHandle, wingIndex, lastSeg, 1., 0.25)
            #Length of the hypothenuse so we do not need atan
            h = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            self.setValueFix(asin((x2 - x1) / h) / rad)

        else:
            self.importError()


    def calc(self):
        '''
        Calculates the quarter chord sweep angle for the horizontal tailplane from the wings sweep
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 42
        '''
        self.setDeviation(0.1182) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        wingSweep = self.parent.aircraft.wing.phi25.getValue()

        return self.setValueCalc(wingSweep + 5.)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################