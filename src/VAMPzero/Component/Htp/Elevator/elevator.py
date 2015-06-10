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
from VAMPzero.Component.Htp.Elevator.Geometry.refArea import refArea
from VAMPzero.Component.Htp.Elevator.Geometry.rootYLocation import rootYLocation
from VAMPzero.Component.Htp.Elevator.Geometry.span import span
from VAMPzero.Component.Htp.Elevator.Geometry.cRoot import cRoot
from VAMPzero.Component.Htp.Elevator.Geometry.cTip import cTip
from VAMPzero.Lib.CPACS.Export.HTP.ControlSurface.Elevator.elevator import createElevator, createStabilizer


class elevator(component):
    '''
    Calculates the area, span, spanwise root location, root chord and tip chord of the elevator.
    The outcome of the calculations is valid for one elevator. 
    Assumes that both elevators are symmetric. 

    :Author: Lisanne van Veen
    '''

    def __init__(self, htp):
        component.__init__(self)
        self.htp = htp
        self.id = 'elevator'
        self.level = 3

        #Geometry Data        
        self.refArea = refArea()
        self.rootYLocation = rootYLocation()
        self.span = span()
        self.cRoot = cRoot()
        self.cTip = cTip()

    ###################################################################################################
    ##Export to CPACS
    ###################################################################################################

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        @param CPACSObj: the CPACS object holding the data for export
        '''
        try:
            createElevator(CPACSObj, self.htp, self)
        except ZeroDivisionError, e:
            self.log.warning('VAMPzero EXPORT: Elevator for HTP could not be created due to "%s"!', e)

        try:
            createStabilizer(CPACSObj, self.htp, self)
        except ZeroDivisionError, e:
            self.log.warning('VAMPzero EXPORT: Stabilizer for HTP could not be created due to "%s"!', e)

        super(elevator, self).cpacsExport(CPACSObj)


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
        