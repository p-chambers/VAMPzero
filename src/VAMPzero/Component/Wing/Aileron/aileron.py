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
from VAMPzero.Component.Wing.Aileron.Geometry.refArea import refArea
from VAMPzero.Component.Wing.Aileron.Geometry.span import span
from VAMPzero.Component.Wing.Aileron.Geometry.tipYLocation import tipYLocation
from VAMPzero.Component.Wing.Aileron.Geometry.cRoot import cRoot
from VAMPzero.Component.Wing.Aileron.Geometry.cTip import cTip
from VAMPzero.Component.Wing.Aileron.Geometry.taperRatio import taperRatio
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Aileron.aileron import createAileron
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD


class aileron(component):
    '''
    Calculates the area, span, spanwise tip location, root chord and tip chord of the aileron.
    The outcome of the calculations is valid for one aileron. 
    Assumes that both ailerons are symmetric.     

    :Author: Lisanne van Veen
    '''

    def __init__(self, wing):
        component.__init__(self)
        self.wing = wing
        self.id = 'aileron'
        self.level = 3

        #Geometry Data        
        self.refArea = refArea()
        self.span = span()
        self.tipYLocation = tipYLocation()
        self.cRoot = cRoot()
        self.cTip = cTip()
        self.taperRatio = taperRatio()

    ###################################################################################################
    ##Export to CPACS
    ###################################################################################################

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        @param CPACSObj: the CPACS object holding the data for export
        '''
        if self.wing.LoD.getValue() == WING_LOD.ADVDOUBLE or self.wing.LoD.getValue() == WING_LOD.SBW:
            createAileron(CPACSObj, self.wing, self)
        super(aileron, self).cpacsExport(CPACSObj)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
        