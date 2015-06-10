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
from VAMPzero.Component.Airfoil.Aerodynamic.aType import aType
from VAMPzero.Component.Airfoil.Aerodynamic.clMAX import clMAX
from VAMPzero.Component.Airfoil.Aerodynamic.ctm import ctm
from VAMPzero.Component.Airfoil.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Airfoil.Aerodynamic.tc import tc
from VAMPzero.Handler.Component import component


class airfoil(component):
    '''
    .. todo:: 
    
       component airfoil think about using airfoil 
       as an abstract class and inheriting it 
       everytime you create wing and htp,vtp airfoils
    
    '''

    def __init__(self, wing, position=''):
        component.__init__(self)
        self.wing = wing
        self.id = self.wing.id + position + 'airfoil'
        self.position = position
        self.level = 3

        self.aType = aType()

        #Geometry Data        
        self.tc = tc()
        self.ctm = ctm()

        #Aero Data
        self.reynoldsNr = reynoldsNr()
        self.clMAX = clMAX()


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
        