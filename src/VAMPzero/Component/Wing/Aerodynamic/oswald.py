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
from cmath import cos, pi, sin
from scipy import polyfit

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.general import chunks, interpolateList, \
    findLower, findHigher
from VAMPzero.Lib.TIXI.tixi import openTIXI, getText, getList


rad = pi / 180.


class oswald(parameter):
    '''
    The Oswald efficiency, similar to the span efficiency, is a correction factor that represents
    the change in drag with lift of a three dimensional wing or airplane, as compared with an ideal
    wing having the same aspect ratio and an elliptical lift distribution.
    
    This part of the Oswald factor calculation relates to the calculation of a theoretical lift factor for the
    wing of the aircraft. Further corrections are made for the Oswald factor on aircraft level. 

    :Unit: [ ]

    :Wiki: http://en.wikipedia.org/wiki/Oswald_efficiency_number
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(oswald, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameter's cpacsImport method!
        Will get the value for the Oswald Factor from CPACS
        It will be assumed that the aeroperformanceMap holds LiLi values
        Does a monkey patch as it replaces oswald.calc with oswald.calcLiLi

        .. todo:: 

            cpacsImport oswald catch error if cfy is unequal zero
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

    def calcRaymer(self):
        '''
        Calculates the oswald factor for the wing. The method is taken from Raymer's book. 
        It is based on the aspectRatio of the wing and the sweep of the wing. 

        Two different formulas are applied one for a swept back wing and one for an unswept wing. 
        The formula for the swept back wing is only taken into account for sweep angles larger than 30deg. 

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 299
        '''
        aspectRatio = self.parent.aspectRatio.getValue()
        # phi25          = self.parent.phi25.getValue()
        phiLE = self.parent.phiLE.getValue()

        if phiLE > 30.:
            # @todo: calc oswald: Catch error for phiLe < 30deg s. Raymer p. 303 in Oswald Calculation 
            # phiLE           = self.parent.phiLE.getValue()
            return self.setValueCalc(4.61 * (1 - 0.045 * aspectRatio ** 0.68) * (cos(phiLE * rad)) ** 0.15 - 3.1)
        else:
            return self.setValueCalc(1.78 * (1 - 0.045 * aspectRatio ** 0.68) - 0.64)


    def calcCEAS(self):
        '''
        This calculation is based on a multi-fidelity study that we did for the CEAS conference in 2011.
	    We ran a set of 500 LIFTING_LINE calculations and applied a symbolic regression application named
	    Eurequa to the data that we obtained. The design space of this equation is:
        
        * taperRatio 0.1 - 0.6
        * phi25 -20deg - 30 deg
        * aspectRatio 6 - 16
	    * twist -10 - 0
	    * kinkRatio 0.2-0.4
        
        :Source: An Integrated Method for the Determination of the Oswald Factor in a Multi-Fidelity Design Environment, D. Boehnke, J. Jepsen, B. Nagel, V. Gollnick, C. Liersch, CEAS 2011
	    :Source: Distilling Free-Form Natural Laws from Experimental Data, M. Schmidt , H. Lipson, Science, Vol. 324, no. 5923, pp. 81 - 85., 2009
	    :Source: Ein Mehrfach-Traglinienverfahren und seine Verwendung fuer Entwurf und Nachrechnung nichtplanarer Fluegelanordnungen, K. H. Horstmann, DFVLR-FB 87-51, 1987
        '''

        taperRatio = self.parent.taperRatio.getValue()
        phi = self.parent.phi25.getValue()
        aspectRatio = self.parent.aspectRatio.getValue()
        eta = self.parent.etaKink.getValue()
        twist = self.parent.twist.getValue()

        t1 = 0.04 - 0.0007 * aspectRatio - 0.00019 * phi * twist
        t2 = 0.16 - 0.0007 * aspectRatio * phi - 0.0007 * aspectRatio * phi * eta - 0.55 * taperRatio
        t3 = taperRatio ** 0.03 * cos(t2 * rad)

        return self.setValueCalc(t1 + t3)

    def calc(self):
        """
        :Source: Daniel's Thesis
        """
        taperRatio = self.parent.taperRatio.getValue()
        phi = self.parent.phi25.getValue()*rad
        aspectRatio = self.parent.aspectRatio.getValue()
        eta = self.parent.etaKink.getValue()
        twist = self.parent.twist.getValue()*rad
        
        res = cos(.422+.154*twist - 0.0126*aspectRatio - 0.53 * taperRatio-.199*aspectRatio * eta * phi)
        return self.setValueCalc(res)
        
    def calcLiLi(self):
        '''
        calculates the Oswald factor for the wing from LIFTING_LINE input read from CPACS. 
        LIFTING_LINE is a multiple lifting-line code attached to CPACS. It computes the lift induced drag. 

        The aeroPerformanceMap created by LIFTING_LINE was imported by the cpacsImport method, if this method is triggered.
        A quadratic polynom will be fitted to the aeroPerformanceMap to find the Oswald factor. 

        :Source: Ein Mehrfach-Traglinienverfahren und seine Verwendung fuer Entwurf und Nachrechnung nichtplanarer Fluegelanordnungen, K. H. Horstmann, DFVLR-FB 87-51, 1987
        '''

        #=======================================================
        # Getting
        #=======================================================
        aspectRatio = self.parent.aspectRatio.getValue()
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

                # Cut the lists to the Machnumber we are using 
                cfx = list(chunks(self.CfxList, pMach))[i]
                cfz = list(chunks(self.CfzList, pMach))[i]

            except:
                self.log.debug("VAMPzero Calc: Cruise MachNumber is not part of the imported CPACS data!")

                x1 = findLower(machCr, self.machList)
                x2 = findHigher(machCr, self.machList)
                if not x1 or not x2:
                    self.log.warn(
                        'VAMPzero MATH: AeroperformanceMap is out of bounds for calculation of the oswald factor. Can not find corresponding mach number')

                y1 = list(chunks(self.CfxList, pMach))[self.machList.index(x1)]
                y2 = list(chunks(self.CfxList, pMach))[self.machList.index(x2)]
                cfx = interpolateList(x1, x2, machCr, y1, y2)

                y1 = list(chunks(self.CfzList, pMach))[self.machList.index(x1)]
                y2 = list(chunks(self.CfzList, pMach))[self.machList.index(x2)]
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

                # Cut the lists to the Machnumber we are using 
                cfx = list(chunks(cfx, n / nRe))[i]
                cfz = list(chunks(cfz, n / nRe))[i]

            except:
                self.log.debug("VAMPzero Calc: wing reynolds number  is not part of the imported CPACS data!")

                x1 = findLower(reynoldsNr, self.reList)
                x2 = findHigher(reynoldsNr, self.reList)
                if not x1 or not x2:
                    self.log.warn(
                        'VAMPzero MATH: AeroperformanceMap is out of bounds for calculation of the oswald factor. Can not find corresponding Reynoldsnumbers')

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

                # Cut the lists to the Machnumber we are using 
                cfx = list(chunks(cfx, n / nAOY))[i]
                cfz = list(chunks(cfz, n / nAOY))[i]

            except:
                self.log.debug("VAMPzero Calc: AOY = 0. is not part of the imported CPACS data!")

                x1 = findLower(0., self.AOYList)
                x2 = findHigher(0., self.AOYList)
                if not x1 or not x2:
                    self.log.warn(
                        'VAMPzero MATH: AeroperformanceMap is out of bounds for calculation of the oswald factor. Can not find corresponding angle of attack')

                y1 = list(chunks(cfx, n / nAOY))[self.AOYList.index(x1)]
                y2 = list(chunks(cfx, n / nAOY))[self.AOYList.index(x2)]
                cfx = interpolateList(x1, x2, reynoldsNr, y1, y2)

                y1 = list(chunks(cfz, n / nAOY))[self.AOYList.index(x1)]
                y2 = list(chunks(cfz, n / nAOY))[self.AOYList.index(x2)]
                cfz = interpolateList(x1, x2, 0., y1, y2)

        #=======================================================================
        # Calculation Oswald and CD0 by quadratic Regression
        #=======================================================================

        cd = [cx*cos(alpha*rad)+cz*sin(alpha*rad) for cx, cz, alpha in zip(cfx, cfz, self.AOAList)]
        ca = [cz*cos(alpha*rad)-cx*sin(alpha*rad) for cx, cz, alpha in zip(cfx, cfz, self.AOAList)]

        (ar, br, CD0) = polyfit(ca, cd, 2)

        if aspectRatio != 0.:
            return self.setValueCalc(1 / (pi * aspectRatio * ar))


###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
