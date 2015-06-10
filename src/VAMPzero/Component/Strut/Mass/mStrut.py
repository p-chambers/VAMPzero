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
from cmath import cos, sqrt, pi

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import checkElement, getText, openTIXI



rad = pi / 180.


class mStrut(parameter):
    '''
    The mass of the struts (sum of both sides). The strut does not include any systems or control surfaces

    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mStrut, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)



    def calc(self):
        '''
        Surrogate model of a finite element analysis

        Limited to the following boundaries
           * wing.aspectRatio = 12. - 17.
           * wing.tcAVG = 0.08 - 0.13
           * wing.twist = -4. - -10.
           * wing.phi25 = 5. - 20.
           * aircraft.mTOM = 60000. - 90000.
           * strut.etaStrut = 0.2 - 0.7
           * strut.depth = 0.1 - 0.2

        :Source: Boehnke, D., A Multi-Fidelity Workflow to Derive Physics-Based Conceptual Design Methods, TUHH, tbp.
        '''
        AR = self.parent.aircraft.wing.aspectRatio.getValue()
        S = self.parent.aircraft.wing.refArea.getValue()
        tc = self.parent.aircraft.wing.tcAVG.getValue()
        sw = self.parent.aircraft.wing.phi25.getValue()*pi/180.
        mTOM = self.parent.aircraft.mTOM.getValue()*pi/180.
        c = self.parent.depth.getValue()
        eta = self.parent.etaStrut.getValue()
        res = 0.02061845578*sw*mTOM + 87.70552679*eta*c*sqrt(AR*S) + S*eta*c*sqrt(AR*S) - 21790.78072*sw*tc*eta
        return self.setValueCalc(res)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
