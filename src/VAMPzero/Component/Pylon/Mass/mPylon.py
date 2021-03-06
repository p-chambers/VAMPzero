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


class mPylon(parameter):
    '''
    The under wing engine pylon mass definition equals the Airbus weight chapter 16. The 
    pylon mass includes the complete pylon structure between the wing and 
    the removable power plant, broken down as follows:
    
    * primary structure
    
       * pylon box (ribs, spars, upper and lower panel, stringers, access doors)
       * forward and rear engine mount (mount fittings, link assy , pin, nut, bearing, thrust rod)
       * forward and rear wing interfaces (link assy, pin, bearing, nut)
       * spigot fittings, fixed support, spar splice
    
    *    secondary structure
    
       * fairings, fairing ribs, sealant, external paint final coat, firewalls, soft mounts
    
    The pylon mass excludes systems (e.g. actuators) but fittings on which e.g. 
    the actuators are fixed are included into the pylon mass but not the 
    bolts that are used for fixing the actuator.
    
    The main difference between the DIN 9020 (which is normally used within LTH) 
    and the Airbus definition is, that pylons and nacelles are accounted within 
    the chapter *nacelle and engine installation* in DIN 9020, while the engine 
    nacelle is accounted within the equipped engine weight (Ch. 20) according to the Airbus accounting.
    
    For the Fokker F100, the pylon mass (according to the Airbus 
    definition) is ~28% of the *nacelle and engine installation* -mass of the 
    DIN 9020 accounting. Pleas note, that the fuselage pylon mass of the F100 is nameable lighter, compared with an under wing pylon.
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mPylon, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)


    def calc(self):
        '''
        For wing mounted engine, sets the calc method to calcBoxBeam;
        For fuselage mounted engine, sets the calc method to calcEmpirical.
        '''

        location = self.parent.aircraft.engine.location.getValue()
        if location:
            self.calc = self.calcBoxBeam
        else:
            self.calc = self.calcEmpirical

    def calcEmpirical(self):
        '''
        calculates the Pylon Mass by empirical method generated by:
        Fokker F28 MK4000	Fokker 70	Fokker 100	MPC75	P316	P317/5
        '''

        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        dEngine = self.parent.aircraft.engine.dEngine.getValue()
        engineM = self.parent.aircraft.engine.mEngine.getValue()
        lPylon = (0.5 + 0.2) * dEngine
        k = 0.066
        return self.setValueCalc(nEngine * engineM *k * lPylon)


    def calcBoxBeam(self):
        '''
        calculates the Pylon Mass 

        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.107) # needs to be set by the calc method when called for later use (deviation depends on the calc method)

        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        thrustTOISA = self.parent.aircraft.engine.thrustTOISA.getValue()

        return self.setValueCalc(nEngine * 0.2648 * (thrustTOISA) ** 0.6517)

    def calcDragStrut(self):
        '''
        calculates the Pylon Mass 

        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.101) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        thrustTOISA = self.parent.aircraft.engine.thrustTOISA.getValue()

        return self.setValueCalc(nEngine * 0.0131 * (thrustTOISA) ** 0.8806)

    def calcDorbathPraktikum(self):
        '''
        calculates the Pylon Mass 

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 141
        '''
        engineM = self.parent.aircraft.engine.mEngine.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()

        return self.setValueCalc(engineM * (0.0000001 * mTOM + 0.11))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################