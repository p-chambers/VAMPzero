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

from math import pi

from VAMPzero.Handler.Parameter import parameter


class mStructure(parameter):
    '''
    The fuselage mass definition equals the Airbus weight chapter 11. The fuselage mass includes the complete fuselage structure, broken down as follows:
    
    * panels (skin shell panels, stringer, doubler, window frames)
    * frames (frames, pressure bulkheads, clips, frame junction fittings)
    * doors (doors, locking mechanism, hinge arm and fittings, door seal)
    * windscreens and windows
    * windscreen and opening frames
    * cabin floor structure
    * cargo compartment floor structure
    * special structures (landing gear bays, keel beam, VTP and HTP attachment, APU attachment)
    * fillet and fairings (belly fairing, leading edge root fillets, upper/lower wing fairing, APU fairing)
    * miscellaneous (external paint final coat, stairs, barrier wall, installation parts)
    
    The fuselage mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators are fixed are included into wing mass but not the bolts, that are used for fixing the actuator.
    
    The main differences between the DIN 9020 (which is normally used within LTH) and the Airbus definition is that all wing-fuselage fairings, landing gear fittings and fittings of subsystems are accounted within the fuselage chapter.
    The fuselage weight of Airbus aircraft is between 0% and 3.4% heavier according to the airbus weight chapter definition and the Fokker F100 is ~6% heavier.

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mStructure, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)
    def calc(self):
        '''
        For wing mounted engine, sets the calc method to calcWingMount;
        For fuselage mounted engine, sets the calc method to calcFuselageMount.
        '''

        location = self.parent.aircraft.engine.location.getValue()
        if location == 1.:
            self.calc = self.calcWingMount
        else:
            self.calc = self.calcFuselageMount


    def calcFuselageMount(self):
        '''
        Calclates the fuselage structure mass from the finess ratio. Note that hfus and wfus as defined in LTH are not available inside VAMPzero and will not be taken into account
        :Source: LTH UL-442.0(T).
        The equation is updated by a factor of (1+k) ** 0.367, where the k value is 0.2 for fuselage mounted engines.
        :Source: LTH MA 508 12-02
        '''
        self.setDeviation(0.063) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        k = 0.2
        exp = 0.367
        dfus = self.parent.dfus.getValue()
        lfus = self.parent.lfus.getValue()

        T1 = 12.7 * (lfus * dfus) ** 1.2982
        T2 = (-0.008 * (lfus / dfus) ** 2 + 0.1664 * lfus / dfus - 0.8501)
        T3 = 1 # should be max(wfus,hfus) / dfus but can not be used in VAMPzero since hfus or wfus are not available

        return self.setValueCalc(T1 * (1 - T2) * T3 * (1 + k) ** exp)


    def calcWingMount(self):
        '''
        Calclates the fuselage structure mass from the finess ratio. Note that hfus and wfus as defined in LTH are not available inside VAMPzero and will not be taken into account
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.063) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
                
        dfus = self.parent.dfus.getValue()
        lfus = self.parent.lfus.getValue()

        T1 = 12.7 * (lfus * dfus) ** 1.2982
        T2 = (-0.008 * (lfus / dfus) ** 2 + 0.1664 * lfus / dfus - 0.8501)
        T3 = 1 # should be max(wfus,hfus) / dfus but can not be used in VAMPzero since hfus or wfus are not available

        return self.setValueCalc(T1 * (1 - T2) * T3)

    def calcDorbathPraktikum(self):
        '''
        Calclates the fuselage structure mass from the area
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 142
        
        .. todo:: 
        
           calcDorbathPraktikum mStructure: add a switch for small fuselages depending on mPayload
        '''
        dfus = self.parent.dfus.getValue()
        lfus = self.parent.lfus.getValue()

        Sfus = dfus * lfus * pi

        return self.setValueCalc(0.011 * Sfus ** 2 + 7.28 * Sfus + 3100)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################