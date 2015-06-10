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
from cmath import sqrt, pi, cos, tan, atan
import numpy as np
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSurfaceArea


class CLalphaHTP_CR(parameter):
    '''
    The derivative of the lift coefficient of the horizontal tailplane for the Cruise.
    
    :Unit: [-]

    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(CLalphaHTP_CR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        :Source: FAR 25.335: Design airspeeds, FAR 25.253 High-speed characteristics)
        '''
        aspectRatioHPT = self.parent.aspectRatio.getValue()
        phi50HTP = self.parent.phi50.getValue()
        machCR = self.parent.aircraft.machCR.getValue()

        delta_MMO = 0.05                   #margin to Maximum Operating Mach Number (MMO) may not less than 0.05
        machCR_MMO = machCR + delta_MMO

        CLalphaHTP = (2 * pi * aspectRatioHPT)/(2 + (aspectRatioHPT**2 * (tan(phi50HTP*pi/180)**2 + 1 - machCR_MMO**2) + 4)**0.5)

        return self.setValueCalc(CLalphaHTP)