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


class mSystems(parameter):
    '''
    The systems mass definition, which is used in this paper, equals the Airbus weight 
    chapter 30 to 42. The system mass includes all following systems:
    
    * auxiliary power unit (APU)
    * hydraulic generation
    * hydraulic distribution
    * air conditioning (generation, distribution, ventilation, pressure control)
    * de-icing and anti-icing (at wing, tail, air intake, windscreen and propellers)
    * fire protection (engine, APU, cargo and landing gear bay fire protection, smoke detection)
    * flight controls (incl. mechanical flight controls (e.g. actuators) and cockpit control mechanisms; excl. cables, electrical control and monitoring items)
    * instrument panels (in the cockpit)
    * automatic flight system
    * navigation (incl. cables, brackets semi-equipment and mountings)
    * communication (incl. cables, brackets semi-equipment and mountings)
    * electrical generation
    * electrical distribution
    
    The system masses exclude fittings on which they are fixed but include the bolts that are used for fixing the systems.
    
    The mass definition between the Airbus accounting and the DIN 9020 (which is normally used within LTH) differs in several points. 
    As first approximation the system mass of the Airbus accounting equals the sum of the following DIN 9020 groups:

    * surface control
    * auxiliary power
    * instruments
    * hydraulic and pneumatic
    * electrical 
    * electronical
    * air-condition and anti-icing (without the bleed air system, which is accounted for in *power units* according to Airbus definition)
    
    Using this approach the difference between both accounting systems is 1.5% for 
    the Fokker F100. Please note, that several detailed differences are not considered in this approach.

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mSystems, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the system mass
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.08) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        lfus = self.parent.aircraft.fuselage.lfus.getValue()

        return self.setValueCalc(42.059 * (lfus * dfus) ** 0.9414)

    def calcDorbathPraktikum(self):
        '''
        Calculates the system mass

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. p149
        '''
        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        lfus = self.parent.aircraft.fuselage.lfus.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()

        fratio = lfus / dfus

        return self.setValueCalc((0.034 * mTOM + 2000) * (1 + 0.5 * (10 - fratio) / 10))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################