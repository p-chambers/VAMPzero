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
from math import e, pi

from numpy.lib.function_base import interp

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement, getText


rad = pi / 180.


class sfcCR(parameter):
    '''
    SFC for cruise condition 

    Specific fuel consumption, SFC, is an engineering term
    that is used to describe the fuel efficiency of an engine 
    design with respect to thrust output. It allows the efficiency 
    of different sized engines to be directly compared.    

    :Unit: [kg/h/N]
    :Wiki: http://en.wikipedia.org/wiki/Thrust_specific_fuel_consumption
    '''

    def __init__(self, value=0., unit='kg/h/N', parent='', cpacsPath=''):
        super(sfcCR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Overwrites the parameters cpacsImport method!

        Imports the enginePerformanceMap

        This method replaces the initial calc method by calcCPACS

        sfcCR will not be set fix because ongoing interpolation is necessary to find
        the correct values
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if checkElement(TIXIHandle, '/cpacs/vehicles/engines/engine[last()]/analysis/performanceMaps/performanceMap'):

            # Get performanceMap from CPACS
            Tmap = getText(TIXIHandle,
                           "/cpacs/vehicles/engines/engine[last()]/analysis/performanceMaps/performanceMap/thrust").split(
                ';')
            Mamap = getText(TIXIHandle,
                            "/cpacs/vehicles/engines/engine[last()]/analysis/performanceMaps/performanceMap/machNumber").split(
                ';')
            FLmap = getText(TIXIHandle,
                            "/cpacs/vehicles/engines/engine[last()]/analysis/performanceMaps/performanceMap/flightLevel").split(
                ';')
            mDotmap = getText(TIXIHandle,
                              "/cpacs/vehicles/engines/engine[last()]/analysis/performanceMaps/performanceMap/mDotFuel").split(
                ';')

            #Pop Last entries because of garbage
            FLmap.pop()
            mDotmap.pop()
            Tmap.pop()
            Mamap.pop()

            #Conversion
            FLmap = [float(val) for val in FLmap]
            Mamap = [float(val) for val in Mamap]
            Tmap = [float(val) for val in Tmap]
            mDotmap = [float(val) for val in mDotmap]

            #Dummies
            maList = []
            flList = []
            thList = []

            #Go Through complete Data Set
            for i in range(len(FLmap)):
                thList.append([Tmap[i - 1], mDotmap[i - 1]])

                if Mamap[i] != Mamap[i - 1]:
                    maList.append([Mamap[i - 1], thList])
                    thList = []

                if FLmap[i] != FLmap[i - 1]:
                    flList.append([FLmap[i - 1], maList])
                    maList = []

            # Final List of List of List for the engine deck
            self.TList = flList

            #set calcTWDat as the new Calculation method
            self.calc = self.calcCPACS
            self.monkeyPatch('CPACS')

        else:
            self.importError()

    def getNearest(self, FLList, FL, MA, T):
        '''
        getNearest is a function to interpolate in a CPACS engine performance map.
        '''

        def getUpLow(List, Target):
            Plus = [99999999., 0]
            Minus = [0., 0]

            for item in List:
                # Set the lower value for the interpolation of Flight Level
                if item[0] - Target > Minus[0] - Target and item[0] - Target < 0.:
                    Minus = item

                # Set the upper value for the interpolation of Flight Level
                if item[0] - Target < Plus[0] - Target and item[0] - Target > 0.:
                    Plus = item

            if List[-1][0] < Target:
                Minus = List[-2]
                Plus = List[-1]
                self.log.warning('VAMPzero SFC: Interpolation Error need to extrapolate! Target value is: %s' % Target)
                self.log.warning('VAMPzero SFC: New up: %s and low: %s' % (Plus[0], Minus[0]))

            return Plus, Minus

        FLplus, FLminus = getUpLow(FLList, FL)

        FLplusMAplus, FLplusMAminus = getUpLow(FLplus[1], MA)
        FLminusMAplus, FLminusMAminus = getUpLow(FLminus[1], MA)

        FLplusMAplusTplus, FLplusMAplusTminus = getUpLow(FLplusMAplus[1], T)
        FLplusMAminusTplus, FLplusMAminusTminus = getUpLow(FLplusMAminus[1], T)
        FLminusMAplusTplus, FLminusMAplusTminus = getUpLow(FLminusMAplus[1], T)
        FLminusMAminusTplus, FLminusMAminusTminus = getUpLow(FLminusMAminus[1], T)

        # Do the interpolations
        SFCFLplusMaplus = interp(T, [FLplusMAplusTminus[0], FLplusMAplusTplus[0]],
                                 [FLplusMAplusTminus[1], FLplusMAplusTplus[1]])
        SFCFLplusMaminus = interp(T, [FLplusMAminusTminus[0], FLplusMAminusTplus[0]],
                                  [FLplusMAminusTminus[1], FLplusMAminusTplus[1]])
        SFCFLminusMaplus = interp(T, [FLminusMAplusTminus[0], FLminusMAplusTplus[0]],
                                  [FLminusMAplusTminus[1], FLminusMAplusTplus[1]])
        SFCFLminusMaminus = interp(T, [FLminusMAminusTminus[0], FLminusMAminusTplus[0]],
                                   [FLminusMAminusTminus[1], FLminusMAminusTplus[1]])

        SFCFLplus = interp(MA, [FLplusMAminus[0], FLplusMAplus[0]], [SFCFLplusMaminus, SFCFLplusMaplus])
        SFCFLminus = interp(MA, [FLminusMAminus[0], FLminusMAplus[0]], [SFCFLminusMaminus, SFCFLminusMaplus])

        SFC = interp(FL, [FLminus[0], FLplus[0]], [SFCFLminus, SFCFLplus])
        return SFC

    def calc(self):
        '''
        Sets the calc method to calcOverallEff
        '''
        self.calc = self.calcOverallEff

    def calcJet(self):
        '''
        calculates the SFC for cruise Condition from the Bypass Ratio
        this method my be replaced by calcTWDat if cpacsImport is called on sfcCR

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 198, Eq. 10.9
        '''
        bypassRatio = self.parent.bypassRatio.getValue()

        ConversionFactor = 3600. / 35303.92683  # to kg/h/N

        return self.setValueCalc((0.88 * e ** (-0.05 * bypassRatio)) * ConversionFactor)

    def calcCPACS(self):
        '''
        This is an alternative Calculation Method for the SFC during Cruise. 
        It relies on the input of a CPACS engine deck. If cpacsImport is called the method will 
        be set as the new calc method
        '''
        altCR = self.parent.aircraft.altCR.getValue()
        machCR = self.parent.aircraft.machCR.getValue()
        thrustCR = self.parent.thrustCR.getValue()
        candidate = self.getNearest(self.TList, altCR, machCR, thrustCR) / thrustCR * 3600

        if candidate < 0.005:
            self.log.warning('VAMPzero CALC: TWDAT seems to return too low candidate. Probably extrapolation issues.')
            self.log.warning('VAMPzero CALC: Will reset SFC_cr to 0.01 to ensure convergence.')
            candidate = 0.01
        elif candidate > 0.1:
            self.log.warning('VAMPzero CALC: TWDAT seems to return too high candidate. Probably extrapolation issues.')
            self.log.warning('VAMPzero CALC: Will reset SFC_cr to 0.1 to ensure convergence.')
            candidate = 0.1

        return self.setValueCalc(candidate)

    def calcOverallEff(self):
        '''
        Calculation Method based on Overall Engine Efficiency

        :Source: Elements of Propulsion: Gas Turbines and Rockets, J.D. Mattingly, AIAA Education Series, 2006, Second Edition, p. 26
        :Author: Momchil Dimchev, TU Delft
        '''
        TAS = self.parent.aircraft.atmosphere.TASCR.getValue()
        etaProp = self.parent.etaProp.getValue()
        etaTransm = self.parent.etaTransm.getValue()
        etaTherm = self.parent.etaTherm.getValue()

        hFuel = 42.80e6  # Standard low heating value for aviation fuel

        overallEff = etaProp * etaTransm * etaTherm

        conversionFactor = 3600  # to kg/h/N
        # conversionFactor = 1e6                # to mg/s/N
        # conversionFactor = 35303.92683        # to lbm/h/lbf

        return self.setValueCalc((TAS / (hFuel * overallEff)) * conversionFactor)

    def calcProp(self):
        '''
        Calculation for Propeller engines
        
        :Source: Aircraft Design, A.K. Kundu, Cambridge Aerospace Series, 2010, p. 349  
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p. 18
        :Author: Marco Friederich, TU Braunschweig
        '''
        Mach = self.parent.aircraft.machCR.getValue()
        Thrust = self.parent.thrustCR.getValue()

        a = 0

        if a == 0:
            Thrust = 1
            a = 1

        etamotor = 0.4
        benoetigteLeistung = (Thrust * Mach * 299.848 / (0.85 * 0.77 * etamotor)) * 3600
        ed = 43.5 * 1000000
        proschub = Thrust / 9.81
        result = benoetigteLeistung / ed / proschub
        return self.setValueCalc(result)