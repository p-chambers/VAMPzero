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
from VAMPzero.Component.Payload.Mass.mCargo import mCargo
from VAMPzero.Component.Payload.Mass.mPax import mPax
from VAMPzero.Component.Payload.Mass.mPayload import mPayload
from VAMPzero.Component.Payload.Mass.mSinglePax import mSinglePax
from VAMPzero.Component.Payload.Mass.paxSeats import paxSeats
from VAMPzero.Component.Payload.Mass.posCoG import posCoG
from VAMPzero.Handler.Component import component


class payload(component):
    '''
    Payload Class
    '''

    def __init__(self, aircraft):
        '''
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'payload'
        self.aircraft = aircraft
        self.level = 2

        #Mass
        self.mPayload = mPayload(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/payload/massDescription/mass')
        self.mCargo = mCargo(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/payload/mCargo/massDescription/mass')
        self.paxSeats = paxSeats(cpacsPath='/cpacs/vehicles/aircraft/model/global/paxSeats')
        self.mPax = mPax()
        self.mSinglePax = mSinglePax()
        #Cog
        self.posCoG = posCoG()

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################