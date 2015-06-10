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


class CLalphaHTP_L(parameter):
    '''
    The derivative of the lift coefficient of the horizontal tailplane for the Landing.
    
    :Unit: [-]

    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(CLalphaHTP_L, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        :Source: FAR 23.73: Reference landing approach speed
        '''
        aspectRatioHPT = self.parent.aspectRatio.getValue()
        phi50HTP = self.parent.phi50.getValue()

        mLM = self.parent.aircraft.mLM.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()
        aAP = self.parent.aircraft.atmosphere.aAP.getValue()
        cLL = self.parent.aircraft.cLL.getValue()
        wingrefArea = self.parent.aircraft.wing.refArea.getValue()


        vS0 = ((2 * mLM * 9.81)/(rhoAP * cLL * wingrefArea))**0.5       #vS0: Stall speed for Maximum Landing Mass
        vL = 1.2 * vS0                                                  #vL: Landing speed
        machL = vL/aAP

        CLalphaHTP = (2 * pi * aspectRatioHPT)/(2 + (aspectRatioHPT**2 * (tan(phi50HTP*pi/180)**2 + 1 - machL**2) + 4)**0.5)

        return self.setValueCalc(CLalphaHTP)
