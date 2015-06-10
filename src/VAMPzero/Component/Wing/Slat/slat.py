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
from VAMPzero.Component.Wing.Slat.Geometry.refArea import refArea
from VAMPzero.Component.Wing.Slat.Geometry.avgChord import avgChord
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Slat.Slat import createSlats
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD


class slat(component):
    '''
    Calculates the area and the average chord of the slats. 
    The area is the total area of all slats of one half of the wing, the average chord
    is the chord derived from this area. 
    Assumes that both wings are symmetric. 

    :Author: Lisanne van Veen
    '''

    def __init__(self, wing):
        component.__init__(self)
        self.wing = wing
        self.id = 'slat'
        self.level = 3

        #Geometry Data        
        self.refArea = refArea()
        self.avgChord = avgChord()

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        @param CPACSObj: the CPACS object holding the data for export
        '''
        if self.wing.LoD.getValue() == WING_LOD.ADVDOUBLE:
            createSlats(CPACSObj, self.wing, self)
        super(slat, self).cpacsExport(CPACSObj)

        ###################################################################################################

        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#

###################################################################################################
        