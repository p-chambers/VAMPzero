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
from VAMPzero.Lib.TIXI.tixi import openTIXI, getText, checkElement


class thrustTWDat(parameter):
    '''
    Scaling factor for TWDat derived from current thrust00 in CPACS and current thrustTO from VAMPzero 	
    
    :Unit: [ ]
	
    .. todo::
	
       Move this one to Tool

    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(thrustTWDat, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        imports the value for thrust00 for the current engine out of TWDat
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if checkElement(TIXIHandle, '/cpacs/vehicles/engines/engine/analysis/thrust00'):
            self.thrust00 = eval(getText(TIXIHandle, '/cpacs/vehicles/engines/engine/analysis/thrust00'))
            self.importSuccess()
        else:
            self.importError()

        if checkElement(TIXIHandle, '/cpacs/vehicles/engines/engine/name'):
            name = getText(TIXIHandle, '/cpacs/vehicles/engines/engine/name')
            if name.find('scaled') != -1:
                self.originalScaling = eval(name.split()[-1])
                self.log.info("VAMPzero TIXI: imported previous scaling factor from TWDat: %s" % self.originalScaling)
            else:
                self.originalScaling = 1.
        else:
            self.importError()

    def calc(self):
        '''
        Calculates the scaling factor for TWDat
        
        This includes the ISA values for the engines necessary thrust
		
        If the ratio is beyond 0.8 and 1.2 it will be cut and a warning message is generated
        '''
        thrustTOISA = self.parent.thrustTOISA.getValue()

        try:
            getattr(self, 'thrust00')
        except AttributeError:
            self.thrust00 = 0.

        try:
            getattr(self, 'originalScaling')
        except AttributeError:
            self.originalScaling = 1.

        if self.thrust00 != 0.:
            scaling = thrustTOISA / self.thrust00 * self.originalScaling


            #TWDat only allows a scaling of +-20% Therefore we need to catch greater deviation
            if scaling < 0.8:
                self.log.warning("VAMPzero CALC: TWDat scaling factor is: %s corrected to 0.8" % str(scaling))
                return self.setValueCalc(0.8)

            elif scaling > 1.2:
                self.log.warning("VAMPzero CALC: TWDat scaling factor is: %s corrected to 1.2" % str(scaling))
                return self.setValueCalc(1.2)

            #        elif scaling > 0.99 and scaling <1.01 and not self.name.find('scaled') == -1:
            #        self.log.warning("VAMPzero CALC: Engine might be correct. Not exporting Scaling Factor for TWDat")
            #        Original


            else:
                return self.setValueCalc(round(scaling, 2))

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################




