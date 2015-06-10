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


class posCoGOEM(parameter):
    '''
    The x position of the center of gravity of the empty aircraft (OEM).
    
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(posCoGOEM, self).__init__(value=value, unit='m', doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the x location for the overall center of gravity for the empty aircraft (OEM).
        '''
        oEM = self.parent.oEM.getValue()
        pylonM = self.parent.pylon.mPylon.getValue()
        landingGearM = self.parent.landingGear.mLandingGear.getValue()

        #Begin with single moments
        Me = self.parent.engine.posCoG.getValue() * self.parent.engine.mEngine.getValue()
        Mw = self.parent.wing.posCoG.getValue() * self.parent.wing.mWing.getValue()
        Mhtp = self.parent.htp.posCoG.getValue() * self.parent.htp.mHtp.getValue()
        Mvtp = self.parent.vtp.posCoG.getValue() * self.parent.vtp.mVtp.getValue()
        Mf = self.parent.fuselage.posCoG.getValue() * self.parent.fuselage.mFuselage.getValue()
        Msys = self.parent.systems.posCoG.getValue() * self.parent.systems.mSystems.getValue()

        #OIM to the fuselage section
        MOIM = self.parent.fuselage.posCoG.getValue() * self.parent.oIM.getValue()

        absPos = (Me + Mw + Mhtp + Mvtp + Mf + MOIM + Msys) / (oEM - pylonM - landingGearM)
        return self.setValueCalc(absPos)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
