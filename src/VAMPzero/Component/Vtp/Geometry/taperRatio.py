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
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingUpperPoint, \
    getWingSegmentCount
from VAMPzero.Lib.CPACS.general import pointDistance


class taperRatio(parameter):
    '''
    The taper ratio of the wing is defined by the ratio of tip to root chord length
    
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(taperRatio, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!
        Will get the value for taperRatio from CPACS via TIGL functions
        '''

        def calcRootLength(tiglHandle, wingIndex):
            '''
            Calculates the length of the root section chord
            '''
            x1, y1, z1 = getWingUpperPoint(tiglHandle, wingIndex, 1, 0, 0)
            x2, y2, z2 = getWingUpperPoint(tiglHandle, wingIndex, 1, 0, 1)

            return pointDistance(x1, y1, z1, x2, y2, z2)

        def calcTipLength(tiglHandle, wingIndex):
            '''
            Calculates the length of the tip section chord
            '''
            lastSegment = getWingSegmentCount(tiglHandle, wingIndex)
            x1, y1, z1 = getWingUpperPoint(tiglHandle, wingIndex, lastSegment, 1, 0)
            x2, y2, z2 = getWingUpperPoint(tiglHandle, wingIndex, lastSegment, 1, 1)

            return pointDistance(x1, y1, z1, x2, y2, z2)

        #=======================================================================
        # 
        #=======================================================================
        #@todo: cpacsImport taperRatio: Think about an import logic for the different wings
        wingIndex = 3
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if not TIGLHandle:
            TIGLHandle = openTIGL(TIXIHandle, self.parent.aircraft.modelUID.getValue())

        if checkElement(TIXIHandle, '/cpacs/vehicles/aircraft/model/wings/wing[3]'):
            rootC = calcRootLength(TIGLHandle, wingIndex)
            tipC = calcTipLength(TIGLHandle, wingIndex)

            self.setValueFix(tipC / rootC)
            self.importSuccess()
        else:
            self.importError()


    def calc(self):
        '''
        .. todo::
        
           calc taperRatio: implement 
        '''
        pass

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################