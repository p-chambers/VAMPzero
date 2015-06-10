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
from VAMPzero.Lib.TIXI.tixi import checkElement, getText, openTIXI


class mHtp(parameter):
    '''
    The horizontal tail plane (HTP) mass definition equals the Airbus weight chapter 13. The HTP mass includes the complete HTP structure from tip to tip, broken down as follows:
    
    * torsion box (skins, spars, ribs, sealants, fuselage attachment)
    * leading edge (skins, ribs, panes)
    * fixed trailing edge (panels, ribs, hinge and actuator fittings)
    * elevators (complete elevator body, hinge and actuator fittings)
    * tips and fairings (tips, fairing supports and fairings)
    * miscellaneous (external paint final coat, HTP-fuselage bolts, torsion box-leading edge and torsion box-trailing edge bolts )
    
    The HTP mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators are fixed are included into wing mass but not the bolts that are used for fixing the actuator.
    
    The difference between the DIN 9020 (which is normally used within LTH) and the Airbus definition is small. In the DIN 9020 definition actuator fittings are excluded in the HTP structure weight but therefore flutter dampers are included into the HTP structural weight. The HTP weight difference of the Fokker F100 is <2% between the two weight breakdowns.
    
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mHtp, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        error = 0

        if checkElement(TIXIHandle,
                        '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[3]/massDescription/mass'):
            self.mWingPrimary = eval(getText(TIXIHandle,
                                             '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[3]/massDescription/mass'))
        else:
            error = 1

        if error == 0 and self.mWingPrimary is not None:
            self.setValueFix(self.mWingPrimary * 2.)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Chooses the calculation method for the mass of the horizontal tail depending
        on the location of the tail
        '''
        location = self.parent.location.getValue()

        if location:
            self.calc = self.calcConventional
        elif not location:
            self.calc = self.calcTTail
        else:
            self.log.warn('VAMPzero HTP: No known value for the location is available. Can not determine the appropriate htp mass method')

    def calcTTail(self):
        '''
        Calculates the mass for horizontal tail in a T-tail setup

        :Source: Derived from statistical data for C-5A, C-141, HFB-320, B727-200, DH121 and DHC-5
        '''

        refArea = self.parent.refArea.getValue()

        return self.setValueCalc(8.6068*refArea**1.3047)


    def calcConventional(self):
        '''
        Calculates the mass for a conventional horizontal tail
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.118) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        refArea = self.parent.refArea.getValue()
        tcAVG = self.parent.tcAVG.getValue()

        if tcAVG != 0. and refArea > 0.:
            return self.setValueCalc(12.908 * refArea ** 1.1868 * (1 + (0.1 - tcAVG) / tcAVG))

    def calcDorbathPraktikum(self):
        '''
        Calculates the mass for horizontal tail for a conventional tail

        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 151
        '''
        refArea = self.parent.refArea.getValue()
        tcAVG = self.parent.tcAVG.getValue()

        if tcAVG != 0. and 34 * refArea - 220 * (1 + 2.3 * (0.105 - tcAVG) / tcAVG) > 0.:
            return self.setValueCalc(34 * refArea - 220 * (1 + 2.3 * (0.105 - tcAVG) / tcAVG))

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################