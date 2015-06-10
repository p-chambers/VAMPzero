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

from VAMPzero.Component.Fuel.Mass.mFM import mFM
from VAMPzero.Component.Fuel.Mass.mFuelCLIMB import mFuelCLIMB
from VAMPzero.Component.Fuel.Mass.mFuelCR import mFuelCR
from VAMPzero.Component.Fuel.Mass.mFuelDESCENT import mFuelDESCENT
from VAMPzero.Component.Fuel.Mass.mFuelMAX import mFuelMAX
from VAMPzero.Component.Fuel.Mass.mFuelRES import mFuelRES
from VAMPzero.Component.Fuel.Mass.mFuelTO import mFuelTO
from VAMPzero.Component.Fuel.Mass.mFuelMAXcenterWT import mFuelMAXcenterWT
from VAMPzero.Component.Fuel.Mass.mFuelMAXinnerWT import mFuelMAXinnerWT
from VAMPzero.Component.Fuel.Mass.mFuelMAXouterWT import mFuelMAXouterWT
from VAMPzero.Component.Fuel.Mass.mFuelMAXTT import mFuelMAXTT
from VAMPzero.Component.Fuel.Mass.TrimTank import TrimTank
from VAMPzero.Component.Fuel.CoG.posCoG import posCoG
from VAMPzero.Component.Fuel.CoG.posCoGcenterWT import posCoGcenterWT
from VAMPzero.Component.Fuel.CoG.posCoGinnerWT import posCoGinnerWT
from VAMPzero.Component.Fuel.CoG.posCoGouterWT import posCoGouterWT
from VAMPzero.Component.Fuel.CoG.posCoGTT import posCoGTT
from VAMPzero.Handler.Component import component


class fuel(component):
    '''
    The fuel component. 
    
    As performance and and mission fuel calculations are lengthy there is a separate 
    component for both fuel and performance.
    
    In this component also the maximum fuel that can be stored in the aircraft is calculated  
    '''

    def __init__(self, aircraft):
        '''
        initializes fuel object
        mostly used for documentation
        establishes link to the aircraft class
        '''
        component.__init__(self)
        self.id = 'fuel'
        self.aircraft = aircraft
        self.level = 2

        #Mass
        self.mFuelMAX = mFuelMAX()
        self.mFuelMAXcenterWT = mFuelMAXcenterWT()
        self.mFuelMAXinnerWT = mFuelMAXinnerWT()
        self.mFuelMAXouterWT = mFuelMAXouterWT()
        self.mFuelMAXTT = mFuelMAXTT()
        self.mFM = mFM(cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/fuel/massDescription/mass')
        self.mFuelCLIMB = mFuelCLIMB()
        self.mFuelDESCENT = mFuelDESCENT()
        self.mFuelCR = mFuelCR()
        self.mFuelTO = mFuelTO()
        self.mFuelRES = mFuelRES()
        self.TrimTank = TrimTank()
        
        # CoG
        self.posCoG = posCoG()
        self.posCoGcenterWT = posCoGcenterWT()
        self.posCoGinnerWT = posCoGinnerWT()
        self.posCoGouterWT = posCoGouterWT()
        self.posCoGTT = posCoGTT()

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################        
    

        