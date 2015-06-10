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
from numpy import polyfit

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.general import chunks, interpolateList, \
    findLower, findHigher
from VAMPzero.Lib.TIXI.tixi import openTIXI, getText, getList


class cDMINoffset(parameter):
    '''
    Modelling the drag polar as CD = k*(CL**2) + b*CL + CD0,
    cDMINoffset would be 'b'. This class was mostly adapted
    from Daniel Boehnke's oswald class. The value is normally
    negative, as the point of minimum drag is at a positive CL.

    :Unit: [ ]

    :Wiki: http://en.wikipedia.org/wiki/Drag_Polar
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cDMINoffset, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameter's cpacsImport method! Will get
        the value for cDMINoffset from a CPACS aeroPerformanceMap.
        Does a monkey patch as it replaces cDMINoffset.calc with cDMINoffset.calcLiLi

        .. todo::

            cpacsImport cDMINoffset catch error if cfy is unequal zero
        '''

        try:
            if not TIXIHandle:
                TIXIHandle = openTIXI(path)

            self.refArea = eval(getText(TIXIHandle, '/cpacs/vehicles/aircraft/model/reference/area'))
            self.CfxList = getList(TIXIHandle, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/cfx')
            self.CfzList = getList(TIXIHandle, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/cfz')
            self.CfyList = getList(TIXIHandle, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/cfy')
            self.AOAList = getList(TIXIHandle,
                                   '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/angleOfAttack')
            self.AOYList = getList(TIXIHandle, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/angleOfYaw')
            self.machList = getList(TIXIHandle, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/machNumber')
            self.reList = getList(TIXIHandle,
                                  '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/reynoldsNumber')

            if self.CfxList:
                self.calc = self.calcLiLi
                self.monkeyPatch('LiftingLine')

        except:
            self.importError()

    def calc(self):
        '''
        If aeroPerformanceMap is not given, set cDMINoffset to 0.
        This will give the same results as previous VAMPzero versions.
        '''

        return self.setValueCalc(0.)

    def calcLiLi(self):
        '''
        calculates cDMINoffset for the wing from a precomputed
        aeroPerformanceMap in CPACS. The aeroPerformanceMap was
        imported by the cpacsImport method, if this method was
        triggered. A quadratic polynomial will be fitted to
        the aeroPerformanceMap to find cDMINoffset.

        :Source: Ein Mehrfach-Traglinienverfahren und seine Verwendung fuer Entwurf und Nachrechnung nichtplanarer Fluegelanordnungen, K. H. Horstmann, DFVLR-FB 87-51, 1987
        '''

        #=======================================================
        # Getting
        #=======================================================
        machCr = self.parent.aircraft.machCR.getValue()
        reynoldsNr = self.parent.reynoldsNr.getValue()

        #=======================================================
        # Finding the number of elements in each vector
        #=======================================================
        if type(self.machList) == int or type(self.machList) == float:
            nMach = 1
        else:
            nMach = len(self.machList)

        if type(self.reList) == int or type(self.reList) == float:
            nRe = 1
        else:
            nRe = len(self.reList)

        if type(self.AOYList) == int or type(self.AOYList) == float:
            nAOY = 1
        else:
            nAOY = len(self.AOYList)

        if type(self.AOAList) == int or type(self.AOAList) == float:
            nAOA = 1
        else:
            nAOA = len(self.AOAList)

        if type(self.CfxList) == int or type(self.CfxList) == float:
            n = 1
        else:
            n = len(self.CfxList)

        pMach = n / nMach

        #=======================================================================
        # Sorting Out the Mach Number
        #
        # Sorting in this sense means there are two ways to go:
        #
        # 1. The easy one: The value we are looking for is actually there,
        #    in this case the list only needs to be chunked from the other values
        # 2. The hard one: We need to interpolate. In this case the next bigger
        #    and the next smaller values need to be found and a new list must be created
        #    by interpolation
        #=======================================================================
        if nMach > 1:
            try:
                i = self.machList.index(machCr)

                #Cut the lists to the Machnumber we are using
                cfx = list(chunks(self.CfxList, n / nMach))[i]
                cfz = list(chunks(self.CfzList, n / nMach))[i]

            except:
                self.log.debug("VAMPzero Calc: Cruise MachNumber is not part of the imported CPACS data!")

                x1 = findLower(machCr, self.machList)
                x2 = findHigher(machCr, self.machList)
                if not x1 or not x2:
                    self.log.warn(
                        'VAMPzero MATH: AeroperformanceMap is out of bounds for calculation of cDMINoffset. Can not find corresponding mach number')

                y1 = list(chunks(self.CfxList, n / nMach))[self.machList.index(x1)]
                y2 = list(chunks(self.CfxList, n / nMach))[self.machList.index(x2)]
                cfx = interpolateList(x1, x2, machCr, y1, y2)

                y1 = list(chunks(self.CfzList, n / nMach))[self.machList.index(x1)]
                y2 = list(chunks(self.CfzList, n / nMach))[self.machList.index(x2)]
                cfz = interpolateList(x1, x2, machCr, y1, y2)

        else:
            cfx = self.CfxList
            cfz = self.CfzList

        #=======================================================================
        # Sorting out the Reynoldsnumber
        #=======================================================================
        n = len(cfx)
        if nRe > 1:
            try:
                i = self.reList.index(reynoldsNr)

                #Cut the lists to the Machnumber we are using
                cfx = list(chunks(cfx, n / nRe))[i]
                cfz = list(chunks(cfz, n / nRe))[i]

            except:
                self.log.debug("VAMPzero Calc: wing reynolds number  is not part of the imported CPACS data!")

                x1 = findLower(reynoldsNr, self.reList)
                x2 = findHigher(reynoldsNr, self.reList)
                if not x1 or not x2:
                    self.log.warn(
                        'VAMPzero MATH: AeroperformanceMap is out of bounds for calculation of cDMINoffset. Can not find corresponding Reynoldsnumbers')

                y1 = list(chunks(cfx, n / nRe))[self.reList.index(x1)]
                y2 = list(chunks(cfx, n / nRe))[self.reList.index(x2)]
                cfx = interpolateList(x1, x2, reynoldsNr, y1, y2)

                y1 = list(chunks(cfz, n / nRe))[self.reList.index(x1)]
                y2 = list(chunks(cfz, n / nRe))[self.reList.index(x2)]
                cfz = interpolateList(x1, x2, reynoldsNr, y1, y2)

        #=======================================================================
        # Sorting out the Angle of Yaw
        #=======================================================================
        n = len(cfx)
        if nAOY > 1:
            try:
                i = self.AOYList.index(0.)

                #Cut the lists to the Machnumber we are using
                cfx = list(chunks(cfx, n / nAOY))[i]
                cfz = list(chunks(cfz, n / nAOY))[i]

            except:
                self.log.debug("VAMPzero Calc: AOY = 0. is not part of the imported CPACS data!")

                x1 = findLower(0., self.AOYList)
                x2 = findHigher(0., self.AOYList)
                if not x1 or not x2:
                    self.log.warn(
                        'VAMPzero MATH: AeroperformanceMap is out of bounds for calculation of cDMINoffset. Can not find corresponding angle of attack')

                y1 = list(chunks(cfx, n / nAOY))[self.AOYList.index(x1)]
                y2 = list(chunks(cfx, n / nAOY))[self.AOYList.index(x2)]
                cfx = interpolateList(x1, x2, reynoldsNr, y1, y2)

                y1 = list(chunks(cfz, n / nAOY))[self.AOYList.index(x1)]
                y2 = list(chunks(cfz, n / nAOY))[self.AOYList.index(x2)]
                cfz = interpolateList(x1, x2, 0., y1, y2)

        #=======================================================================
        # Calculation Oswald, cDMINoffset and CD0 by quadratic Regression
        #=======================================================================
        (ar, br, CD0) = polyfit(self.CfzList, self.CfxList, 2)
        return self.setValueCalc(br)


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
