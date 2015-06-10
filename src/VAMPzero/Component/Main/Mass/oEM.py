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


class oEM(parameter):
    '''
    The max operating empty mass
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(oEM, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the operating empty mass from  componentWeights + Operator Items
        
        Components are:
        
        * wing
        * htp
        * vtp
        * engine
        * pylon
        * systems
        * landing gear
        * fuselage
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.036) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        wingMass = self.parent.wing.mWing.getValue()
        htpMass = self.parent.htp.mHtp.getValue()
        vtpMass = self.parent.vtp.mVtp.getValue()
        engineMass = self.parent.engine.mEngine.getValue()
        fuselageMass = self.parent.fuselage.mFuselage.getValue()
        oIM = self.parent.oIM.getValue()
        landingGear = self.parent.landingGear.mLandingGear.getValue()
        pylonMass = self.parent.pylon.mPylon.getValue()
        systemsMass = self.parent.systems.mSystems.getValue()
        strutMass = self.parent.strut.mStrut.getValue()

        return self.setValueCalc(
            wingMass + htpMass + vtpMass + engineMass + fuselageMass + oIM + landingGear + pylonMass + systemsMass + strutMass)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
