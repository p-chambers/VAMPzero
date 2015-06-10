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

from VAMPzero.Component.Atmosphere.Airport.TAP import TAP
from VAMPzero.Component.Atmosphere.Airport.aAP import aAP
from VAMPzero.Component.Atmosphere.Airport.hAP import hAP
from VAMPzero.Component.Atmosphere.Airport.rhoAP import rhoAP
from VAMPzero.Component.Atmosphere.Airport.sigmaAP import sigmaAP
from VAMPzero.Component.Atmosphere.Cruise.EASCR import EASCR
from VAMPzero.Component.Atmosphere.Cruise.MaCR import MaCR
from VAMPzero.Component.Atmosphere.Cruise.TASCR import TASCR
from VAMPzero.Component.Atmosphere.Cruise.TCR import TCR
from VAMPzero.Component.Atmosphere.Cruise.aCR import aCR
from VAMPzero.Component.Atmosphere.Cruise.hCR import hCR
from VAMPzero.Component.Atmosphere.Cruise.myCR import myCR
from VAMPzero.Component.Atmosphere.Cruise.nyCR import nyCR
from VAMPzero.Component.Atmosphere.Cruise.qCR import qCR
from VAMPzero.Component.Atmosphere.Cruise.rhoCR import rhoCR
from VAMPzero.Component.Atmosphere.Cruise.sigmaCR import sigmaCR
from VAMPzero.Component.Atmosphere.FL100.EASFL100 import EASFL100
from VAMPzero.Component.Atmosphere.FL100.MaFL100 import MaFL100
from VAMPzero.Component.Atmosphere.FL100.TASFL100 import TASFL100
from VAMPzero.Component.Atmosphere.FL100.TFL100 import TFL100
from VAMPzero.Component.Atmosphere.FL100.aFL100 import aFL100
from VAMPzero.Component.Atmosphere.FL100.hFL100 import hFL100
from VAMPzero.Component.Atmosphere.FL100.myFL100 import myFL100
from VAMPzero.Component.Atmosphere.FL100.nyFL100 import nyFL100
from VAMPzero.Component.Atmosphere.FL100.qFL100 import qFL100
from VAMPzero.Component.Atmosphere.FL100.rhoFL100 import rhoFL100
from VAMPzero.Component.Atmosphere.FL100.sigmaFL100 import sigmaFL100
from VAMPzero.Component.Atmosphere.FL1500.EASFL1500 import EASFL1500
from VAMPzero.Component.Atmosphere.FL1500.MaFL1500 import MaFL1500
from VAMPzero.Component.Atmosphere.FL1500.TASFL1500 import TASFL1500
from VAMPzero.Component.Atmosphere.FL1500.TFL1500 import TFL1500
from VAMPzero.Component.Atmosphere.FL1500.aFL1500 import aFL1500
from VAMPzero.Component.Atmosphere.FL1500.hFL1500 import hFL1500
from VAMPzero.Component.Atmosphere.FL1500.myFL1500 import myFL1500
from VAMPzero.Component.Atmosphere.FL1500.nyFL1500 import nyFL1500
from VAMPzero.Component.Atmosphere.FL1500.qFL1500 import qFL1500
from VAMPzero.Component.Atmosphere.FL1500.rhoFL1500 import rhoFL1500
from VAMPzero.Component.Atmosphere.FL1500.sigmaFL1500 import sigmaFL1500
from VAMPzero.Handler.Component import component
from VAMPzero.Component.Atmosphere.Airport.pAP import pAP
from VAMPzero.Component.Atmosphere.Airport.deltaT import deltaT


#@todo: think about implementing functions
class atmosphere(component):
    '''
    standard atmosphere class
    
    divided into several "disciplines" that contain different altitudes and mach numbers
    
    .. todo::
       
       Think about implementing the atmosphere into the lib functions
    '''

    def __init__(self, aircraft):
        '''
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'atmosphere'
        self.aircraft = aircraft
        self.level = 2

        #Airport Level
        self.hAP = hAP()
        self.aAP = aAP()
        self.pAP = pAP()
        self.rhoAP = rhoAP()
        self.sigmaAP = sigmaAP()
        self.TAP = TAP()
        self.deltaT = deltaT()

        #CruiseLevel
        self.aCR = aCR()
        self.EASCR = EASCR()
        self.hCR = hCR()
        self.MaCR = MaCR()
        self.myCR = myCR()
        self.nyCR = nyCR()
        self.qCR = qCR()
        self.rhoCR = rhoCR()
        self.sigmaCR = sigmaCR()
        self.TASCR = TASCR()
        self.TCR = TCR()

        #FL1500
        self.aFL1500 = aFL1500()
        self.EASFL1500 = EASFL1500()
        self.hFL1500 = hFL1500()
        self.MaFL1500 = MaFL1500()
        self.myFL1500 = myFL1500()
        self.nyFL1500 = nyFL1500()
        self.qFL1500 = qFL1500()
        self.rhoFL1500 = rhoFL1500()
        self.sigmaFL1500 = sigmaFL1500()
        self.TASFL1500 = TASFL1500()
        self.TFL1500 = TFL1500()

        #FL100
        self.aFL100 = aFL100()
        self.EASFL100 = EASFL100()
        self.hFL100 = hFL100()
        self.MaFL100 = MaFL100()
        self.myFL100 = myFL100()
        self.nyFL100 = nyFL100()
        self.qFL100 = qFL100()
        self.rhoFL100 = rhoFL100()
        self.sigmaFL100 = sigmaFL100()
        self.TASFL100 = TASFL100()
        self.TFL100 = TFL100()

        #Constants
        self.R_s = 287.05                # spezifische Gaskonstante der Luft
        self.kappa = 1.4                   # Adiabatenkoeff.
        self.g = 9.81                  # Erdbeschnleunigung
        self.beta = 1.458e-6              # Sutherland Konstante
        self.S_Sutherland = 110.4                 # [K] Sutherland Temperatur
        self.HA = [0, 11000, 20000]
        self.gammaH = [-0.0065, 0, 0.001]
        self.TA = [288.15, 216.65, 216.65]
        self.pA = [101325, 22620, 5469]
        self.rhoA = [1.225, 0.3637, 0.0879]

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
