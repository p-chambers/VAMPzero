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
from VAMPzero.Component.Vtp.Rudder.Geometry.refArea import refArea
from VAMPzero.Component.Vtp.Rudder.Geometry.span import span
from VAMPzero.Component.Vtp.Rudder.Geometry.cRoot import cRoot
from VAMPzero.Component.Vtp.Rudder.Geometry.cTip import cTip
from VAMPzero.Lib.CPACS.Export.VTP.ControlSurface.Rudder.rudder import createRudder


class rudder(component):
    '''
    Calculates the area, root chord and tip chord of the rudder.
    Assumes that the span of the rudder is equal to the span of the vtp.
    This assumption constrains the location of the rudder. 
                  
    :Author: Lisanne van Veen
    '''

    def __init__(self, vtp):
        component.__init__(self)
        self.vtp = vtp
        self.id = 'rudder'
        self.level = 3

        #Geometry Data        
        self.refArea = refArea()
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
            createRudder(CPACSObj, self.vtp, self)
        except ZeroDivisionError, e:
            self.log.warning('VAMPzero EXPORT: Rudder for VTP could not be created due to "%s"!', e)
        super(rudder, self).cpacsExport(CPACSObj)

        ###################################################################################################

        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#

###################################################################################################
        