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


class mVtp(parameter):
    '''
    The vertical tail plane (VTP) mass definition equals the Airbus weight chapter 14. 
    The VTP mass includes the complete VTP structure, broken down as follows:
    
    * torsion box (skins, spars, ribs, sealants, fuselage attachment)
    * leading edge (dorsal fin, skins, ribs, panes)
    * fixed trailing edge (panels, ribs, hinge and actuator fittings)
    * rudders (complete rudder body, hinge and actuator fittings)
    * tips and fairings (tips, fairing supports and fairings)
    * miscellaneous (external paint final coat, VTP-fuselage bolts, torsion box-leading edge and torsion box-trailing edge bolts )
    
    The VTP mass excludes systems (e.g. actuators) but fittings on which e.g. the actuators 
    are fixed are included into wing mass but not the bolts that are used for fixing the actuator.
    
    The difference between the DIN 9020 (which is normally used within LTH) and the Airbus 
    definition is small. In the DIN 9020 definition actuator fittings are excluded in the VTP 
    structure weight but therefore flutter dampers are included into the VTP structural weight. 
    The VTP weight difference of the Fokker F100 is <2% between the two weight breakdowns.

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mVtp, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        error = 0

        if checkElement(TIXIHandle,
                        '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[5]/massDescription/mass'):
            self.mWingPrimary = eval(getText(TIXIHandle,
                                             '/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure[5]/massDescription/mass'))
        else:
            error = 1

        if error == 0 and self.mWingPrimary is not None:
            self.setValueFix(self.mWingPrimary)
            self.importSuccess()
        else:
            self.importError()

    def calc(self):
        '''
        Chooses the calculation method for the mass of the horizontal tail depending
        on the location
        '''
        location = self.parent.aircraft.htp.location.getValue()

        if location:
            self.calc = self.calcConventional
        elif not location:
            self.calc = self.calcTTail
        else:
            self.log.warn('VAMPzero VTP: No known value for the location of the htp is available. Can not determine the appropriate vtp mass method')

    def calcTTail(self):
        '''
        Calculates the mass for horizontal tail in a T-tail setup

        :Source: Derived from statistical data for C-5A, C-141, HFB-320, B727-200, DH121 and DHC-5
        '''

        refArea = self.parent.refArea.getValue()

        return self.setValueCalc(6.8662*refArea**1.3649)

    def calcConventional(self):
        '''
        Calculates the vertical tail mass
        
        :Source: LTH UL-442.0(T).
        '''
        self.setDeviation(0.12) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        refArea = self.parent.refArea.getValue()

        return self.setValueCalc(25.056 * refArea ** 1.0033)

    def calcDorbathPraktikum(self):
        '''
        Calculates the vertical tail mass for a conventional tail
        switched back to the old equation in the same source due to non negative values!!! 
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p. 151
        '''
        refArea = self.parent.refArea.getValue()

        return self.setValueCalc(0.03 * refArea ** 2 + 25 * refArea)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################