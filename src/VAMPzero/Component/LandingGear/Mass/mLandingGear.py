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
from cmath import atan, pi

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, getText, checkElement


rad = pi / 180.


class mLandingGear(parameter):
    '''
    The landing gear mass definition equals the Airbus weight chapter 15. 
    The landing gear mass includes all landing gears (nose, center and wing landing gears). 
    The formula below is only valid for aircraft having no or one center landing gear. 
    The mass definition is broken down as follows:
    
    * structure (incl. main structure, front and rear pintle pins, upper and lower cardan pins, shock absorber, lock and retraction actuators, fluids in actuators)
    * wheels, brakes and tires
    * miscellaneous (brake system equipment, uplock box, system hydraulic fluids, torque link damper, tachometer, kneeling system equipment, remote data concentrators)
    
    The main differences between the DIN 9020 (which is normally used within LTH) 
    and the Airbus definition is that the wing/fuselage attachment fittings 
    are accounted within the wing/fuselage chapter according to the Airbus definition, but 
    are accounted with the landing gear according to DIN 9020.
    
    For the Fokker F 100 the landing gear weight is ~17% lighter according to 
    the Airbus definition compared with the DIN 9020 definition.
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mLandingGear, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                           cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        imports the values for summed up Nose and Main Landing Gear and set value to fix

        .. todo:: 
           
           cpacsImport mLandingGear this is out dated since LGDesign does not apply to CPACS 1.4
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        error = 0

        if checkElement(TIXIHandle,
                        '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/landingGear/mainGears/mainGear/totalMass/mass'):
            self.mMainGear = eval(getText(TIXIHandle,
                                          '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/landingGear/mainGears/mainGear/totalMass/mass'))
        else:
            error = 1

        if checkElement(TIXIHandle,
                        '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/landingGear/noseGears/noseGear/totalMass/mass'):
            self.mNoseGear = eval(getText(TIXIHandle,
                                          '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/landingGear/noseGears/noseGear/totalMass/mass'))
        else:
            error = 1

        if not error:
            self.setValueFix(2 * self.mMainGear + self.mNoseGear)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        calculates the Landing Gear Mass
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.074) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        mLM = self.parent.aircraft.mLM.getValue()

        return self.setValueCalc(1.8 * 10 ** (-3) * mLM ** 1.278)

    def calcDorbathPraktikum(self):
        '''
        calculates the Landing Gear Mass
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p.150
        '''
        mTOM = self.parent.aircraft.mTOM.getValue()

        return self.setValueCalc(0.000000002 * mTOM ** 2 + 0.04 * mTOM)

        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
