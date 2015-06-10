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
from VAMPzero.Handler.Component import component
from VAMPzero.Component.Wing.Flap.Geometry.refArea import refArea
from VAMPzero.Component.Wing.Flap.Geometry.avgChordInnerFlap import avgChordInnerFlap
from VAMPzero.Component.Wing.Flap.Geometry.spanInnerFlap import spanInnerFlap
from VAMPzero.Component.Wing.Flap.Geometry.refAreaInnerFlap import refAreaInnerFlap
from VAMPzero.Component.Wing.Flap.Geometry.refAreaOuterFlap import refAreaOuterFlap
from VAMPzero.Component.Wing.Flap.Geometry.avgChordOuterFlap import avgChordOuterFlap
from VAMPzero.Component.Wing.Flap.Geometry.spanOuterFlap import spanOuterFlap
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Flap.Flap import createFlaps
from VAMPzero.Component.Wing.Flap.Aerodynamic.dCLmaxTO import dCLmaxTO
from VAMPzero.Component.Wing.Flap.Aerodynamic.dCLmaxL import dCLmaxL
from VAMPzero.Component.Wing.Flap.Aerodynamic.dCDTO import dCDTO
from VAMPzero.Component.Wing.Flap.Aerodynamic.dCDL import dCDL
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD


class flap(component):
    '''
    Calculates the total flap area, and the span, area and average chord of the inner and outer flap.
    Assumes that each aircraft has two flaps and that both wings are symmetric.
    All equations are therefore applicable to one half of the wing.

    :Author: Lisanne van Veen
    '''

    def __init__(self, wing):
        component.__init__(self)
        self.wing = wing
        self.id = 'flap'
        self.level = 3

        #Geometry Data        
        self.refArea = refArea()
        self.avgChordInnerFlap = avgChordInnerFlap()
        self.spanInnerFlap = spanInnerFlap()
        self.refAreaInnerFlap = refAreaInnerFlap()
        self.refAreaOuterFlap = refAreaOuterFlap()
        self.avgChordOuterFlap = avgChordOuterFlap()
        self.spanOuterFlap = spanOuterFlap()

        #Aerodynamic Data
        self.dCLmaxTO = dCLmaxTO()
        self.dCLmaxL = dCLmaxL()
        self.dCDTO = dCDTO()
        self.dCDL = dCDL()


    ###################################################################################################
    ##Export to CPACS
    ###################################################################################################

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        @param CPACSObj: the CPACS object holding the data for export
        '''
        if self.wing.LoD.getValue() == WING_LOD.ADVDOUBLE or self.wing.LoD.getValue() == WING_LOD.SBW:
            createFlaps(parentWingCPACS=CPACSObj, parentWingVAMPzero=self.wing, myFlap=self, typeOfSeg=self.wing.LoD.getValue())
        super(flap, self).cpacsExport(CPACSObj)

        ###################################################################################################

        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#

###################################################################################################
        