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
from cmath import pi, tan

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class xLandingGear(parameter):
    '''
    The x-position of the landing gear
    
    :Unit: [m]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(xLandingGear, self).__init__(value=value, unit='', doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the x-position of the landing gear with respekt to the eta- and xsi-coordinate of the wing.
        '''    
        span = self.parent.aircraft.wing.span.getValue()
        xRoot = self.parent.aircraft.wing.xRoot.getValue()
        cRoot = self.parent.aircraft.wing.cRoot.getValue()
        cTip = self.parent.aircraft.wing.cTip.getValue()
        phiLE = self.parent.aircraft.wing.phiLE.getValue()
        etaLG = self.parent.eta.getValue()
        xsiLG = self.parent.xsi.getValue()
        
        xLG = xRoot + span/2 * tan(phiLE*rad) * etaLG + xsiLG * (span/2 * tan(phiLE*rad) * (1-etaLG) + cTip - (span/2 * tan(phiLE*rad) + cTip - cRoot) * (1-etaLG))     

        return self.setValueCalc(xLG)
###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################