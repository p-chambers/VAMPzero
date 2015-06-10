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
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSegmentCount, \
    getWingUpperPoint
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from cmath import sqrt

class etaEngine(parameter):
    '''
    The eta coordinate of the engine on the wing. This parameter is recognised for the export of wing geometries
    
    :Unit: [ ]
    '''
    
    def __init__(self,value=0.,unit='' ,parent='',cpacsPath =''):
        super(etaEngine,self).__init__(value=value, unit=unit, doc = self.__doc__, status='init',parent = parent, cpacsPath = cpacsPath)

            
    def calc(self):
        '''
        Calculates the etaEngine paramter from the y position of the engine and the span of the wing.
        ''' 
        yEngine     = self.parent.aircraft.engine.yEngine.getValue()
        span        = self.parent.span.getValue()
        
        
        return self.setValueCalc(yEngine/span*2.)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################