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
from cmath import cos, sqrt, pi, log, exp

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import checkElement, getText, openTIXI
import numpy as np

rad = pi / 180.


class mWing(parameter):
    '''
    The wing mass definition equals the Airbus weight chapter 10. The wing mass includes the complete wing structure
    from tip to tip including centre wing box, broken down as follows:

    * skins (including stringers)
    * spars
    * ribs
    * pylon attachments (front and rear attachment, fairing attachments, spigot attachment)
    * landing gear support (gear beam and ribs, attachments and fittings)
    * fixed leading edge (ribs, panels, movable support structures)
    * movable leading edge (slat, droop nose, krueger flaps, slat tracks)
    * fixed trailing edges (panels, falsework, flap tracks and attachments, spoiler and aileron support)
    * movable trailing edges (flaps including flap track rear link and carriages, ailerons and spoiler)
    * miscellaneous (external paint final coat, wing tips, winglets, sealant, fairings, fittings and supports)

    The wing mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators are fixed are included
    into wing mass but not the bolts, that are used for fixing the actuator.

    The main differences between the DIN 9020 (which is normally used within LTH) and the Airbus definition is
    that the wing-fuselage (belly) fairing as well as the landing gear doors in the belly fairing area is not
    accounted within the wing chapter. On the other hand the tank sealant, wing landing gear and pylon fittings and
    fittings of subsystems is accounted within the wing chapter.
    The wing weight of Airbus aircraft is ~1% lighter according to the Airbus weight chapter definition and
    the Fokker F100 is ~2% heavier.

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mWing, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        Imports the values for the primary wing structure and applies formula to calculate mWing
        Value is set to FIX, but a correction factor is applied to get secondary wing mass from
        the imported primary wing structure mass.
        
        :Source: Analytical Fuselage and Wing Weight Estimation of Transport Aircraft, M. D. Ardema, M. C. Chambers, A. P. Patron, A. S. Hahn, H. Miura, M. D. Moore, NASA Technical Memorandum 110392, 1996, p. 22 eq. 109
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        error = 0

        if checkElement(TIXIHandle,
                        '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[1]/massDescription/mass'):
            self.mWingPrimary = eval(getText(TIXIHandle,
                                             '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[1]/massDescription/mass'))
        else:
            error = 1

        if error == 0 and self.mWingPrimary is not None:
            self.setValueFix(2. * self.mWingPrimary)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Determines the appropriate wing mass estimation method based on the strut or not

        CalcStrut and CalcDiss are currently being used
        '''
        strut = self.parent.aircraft.strut.active.getValue()
        if strut:
            self.calc = self.calcStrut
        else:
            self.calc = self.calcDiss

    def calcStrut(self):
        '''
        calculates the Wings Mass if a strut is present. This formula has been derived from a multi-fidelity workflow. The
        calculation is valid in the following boundaries

        wing.aspectRatio = 12. - 17.
        wing.tcAVG = 0.1 - 0.14
        wing.twist = -4. - -10.
        wing.phi25 = 10. - 25.
        aircraft.mTOM = 60000. - 90000.
        strut.etaStrut = 0.5 - 0.75
        strut.depth = 0.1 - 0.2

        :Source: A multi-fidelity workflow to derive physics based conceptual design methods, D. Boehnke, DLR, 2015
        '''

        sweep = self.parent.phi25.getValue()/180.*pi
        aspectRatio = self.parent.aspectRatio.getValue()
        tc = self.parent.tcAVG.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        refArea = self.parent.refArea.getValue()
        twist = self.parent.twist.getValue()
        etaStrut = self.parent.aircraft.strut.etaStrut.getValue()

        mWing = (1.144*10**-4*aspectRatio**2*mTOM-76.91*aspectRatio)/(aspectRatio*tc*etaStrut-twist*etaStrut-7.698*10**-3*aspectRatio)+39.35*refArea+130.2*sweep*tc*refArea
        return self.setValueCalc(mWing)

    def calcDiss(self):
        '''
        calculates the Wings Mass
        
        :Source: A multi-fidelity workflow to derive physics based conceptual design methods, D. Boehnke, DLR, 2015
        '''
        #self.setDeviation(0.062) # needs to be set by the calc method when called for later use (deviation depends on the calc method)

        SW = self.parent.phi25.getValue()*pi/180
        AR = self.parent.aspectRatio.getValue()
        TC = self.parent.tcAVG.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        Aref = self.parent.refArea.getValue()
        WS = mTOM/Aref
        res = 353.9*AR*WS**0.1699*cos(2.178*TC*log(AR))/(cos(SW)*exp(1.96e-7*SW*AR**3.452/TC**2.918))
        return self.setValueCalc(0.0123*res*Aref-0.42*res)
                      
    def calcLTH(self):
        '''
        calculates the Wings Mass
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.062) # needs to be set by the calc method when called for later use (deviation depends on the calc method)

        phi25 = self.parent.phi25.getValue()
        AR = self.parent.aspectRatio.getValue()
        tcAVG = self.parent.tcAVG.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        Aref = self.parent.refArea.getValue()

        phiTerm = 1 / cos(phi25 * rad)
        tcTerm = 1 / sqrt(tcAVG)

        return self.setValueCalc(2.20013 * 10 ** -4 * (401.146 * Aref ** 1.31 + mTOM ** 1.1038) * tcTerm * AR ** 1.5 * phiTerm)

    def calcDorbathPraktikum(self):
        '''
        calculates the Wings Mass
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 146
        '''
        phi25 = self.parent.phi25.getValue()
        AR = self.parent.aspectRatio.getValue()
        tcAVG = self.parent.tcAVG.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        Aref = self.parent.refArea.getValue()

        phiterm = (1. - 0.15 * (29. - phi25 ) / phi25 )
        ARterm = (1. - 0.6 * (8.7 - AR) / AR)
        tcterm = (1. + 0.45 * (0.105 - tcAVG) / tcAVG)

        return self.setValueCalc(
            1.055 * (0.6 * (100 * Aref - 3700) + (1 - 0.6) * (0.135 * mTOM - 1900)) * tcterm * ARterm * phiterm)


    def calcRaymer(self):
        '''
        calculates the Wings Mass
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.399, eq. 15.25
        '''
        S = self.parent.refArea.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        tcRoot = self.parent.tcAVG.getValue()
        AR = self.parent.aspectRatio.getValue()
        phi25 = self.parent.phi25.getValue()
        n = 3.75
        taperRatio = self.parent.taperRatio.getValue()
        Scs = 80.

        mTOM = mTOM * 2.204
        S = S * 3.281 ** 2

        return self.setValueCalc(
            0.0051 * (mTOM * n) ** 0.557 * S ** 0.649 * AR ** .5 * tcRoot ** -0.4 * (1 + taperRatio) ** .1 * 1 / cos(
                phi25 * rad) * Scs ** .1)

    def calcShevell(self):#
        '''
        calculates the Wings Mass
        
        :Source: Fundamentals of Flight, R. S. Shevell, Prentice Hall, 1988, p. 392
        '''
        S = self.parent.refArea.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        tc = self.parent.tcAVG.getValue()
        aspectRatio = self.parent.aspectRatio.getValue()
        phi50 = self.parent.phi50.getValue()
        n = 3.75
        taperRatio = self.parent.taperRatio.getValue()
        mZFW = self.parent.aircraft.mZFW.getValue()

        b = (S * aspectRatio) ** .5

        return self.setValueCalc(45. * S + (n * b ** 3. * (mTOM * mZFW) ** 0.5 * (1. + 2. * taperRatio)) / (
            tc * (cos(phi50 * rad)) ** 2. * S * (1. + taperRatio)) * 1e-6 * 3.)

    def calcToreenbeek(self):#
        '''
        calculates the Wings Mass
        
        :Source: Synthesis of Subsonic Airplane Design, E. Torenbeek, Delft University Press, 1982, p.280
        '''

        S = self.parent.refArea.getValue()
        tcRoot = self.parent.tcAVG.getValue()
        aspectRatio = self.parent.aspectRatio.getValue()
        phi50 = self.parent.phi50.getValue()
        n = 3.75
        mZFW = self.parent.aircraft.mZFW.getValue()

        b = (S * aspectRatio) ** .5
        bref = 1.905                 #reference span
        kw = 6.67e-3               #factor
        bs = b / (cos(phi50 * rad))    #structural span
        k2 = 0.95                  #wing mounted engine

        return self.setValueCalc(
            k2 * kw * bs ** 0.75 * (1 + (bref / bs) ** 0.5) * n ** .55 * ((bs / tcRoot) / (mZFW / S)) ** 0.3 * mZFW)

    def calcEureqa(self):
        '''
        calculates the wing's mass from a method derived from PESTWing
        '''
        Sweep = self.parent.phi25.getValue()
        AspectRatio = self.parent.aspectRatio.getValue()
        Thickness = self.parent.tcAVG.getValue()
        TaperRatio = self.parent.taperRatio.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        S = self.parent.refArea.getValue()

        result = (-8.53e4 * AspectRatio - 6.374 * AspectRatio * mTOM) / (
            209.6 * TaperRatio + 20.76 * AspectRatio + Sweep * Sweep * Thickness - 419.1 - 4739 * Thickness)
        result = (S + result / S) ** 1.73
        return self.setValueCalc(result)


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
