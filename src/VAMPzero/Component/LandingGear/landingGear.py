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
from VAMPzero.Component.LandingGear.Mass.mLandingGear import mLandingGear
from VAMPzero.Component.LandingGear.Position.eta import eta
from VAMPzero.Component.LandingGear.Position.xsi import xsi
from VAMPzero.Component.LandingGear.Position.xLandingGear import xLandingGear
from VAMPzero.Component.LandingGear.Position.yLandingGear import yLandingGear
from VAMPzero.Component.LandingGear.Position.zLandingGear import zLandingGear
from VAMPzero.Component.LandingGear.Position.xNoseGear import xNoseGear
from VAMPzero.Handler.Component import component
from VAMPzero.Component.LandingGear.Aerodynamic.dCDextendedLG import dCDextendedLG


class landingGear(component):
    '''
    Landing Gear Class
    '''

    def __init__(self, aircraft):
        '''
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'landingGear'
        self.aircraft = aircraft
        self.level = 2

        #Parameters
        self.mLandingGear = mLandingGear(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mLandingGears/massDescription/mass')
        self.eta = eta()
        self.xsi = xsi()
        self.xLandingGear = xLandingGear()
        self.yLandingGear = yLandingGear()
        self.zLandingGear = zLandingGear()
        self.xNoseGear = xNoseGear()

        #Aerodynamic
        self.dCDextendedLG = dCDextendedLG()

        ###################################################################################################

#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
