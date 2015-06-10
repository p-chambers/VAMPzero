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


class posNP(parameter):
    '''
    The x-position of the neutral point relative to cMAC
    
    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(posNP, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the position of the neutral point relative to the mean aerodynamic chord
        
        :Source: Einfuehrung in die Luftfahrttechnik, R. Voit-Nitschmann, Uni Stuttgart, 2003, p. 107
        '''
        Cah = self.parent.htp.cLalpha.getValue()
        Caw = self.parent.wing.cLalpha.getValue()
        Sh = self.parent.htp.refArea.getValue()
        Sw = self.parent.wing.refArea.getValue()
        detadalpha = self.parent.htp.detadalpha.getValue()
        cMAC = self.parent.wing.cMAC.getValue()
        cMAChtp = self.parent.htp.cMAC.getValue()
        xMAC = self.parent.wing.xMAC.getValue()
        r0 = self.parent.htp.xMAC.getValue() + 0.25 * cMAChtp - (xMAC + 0.25 * cMAC)

        temp = Sh / Sw * Cah / Caw * (1 - detadalpha)
        temp2 = temp * r0 / cMAC / (1 + temp) + 0.25

        return self.setValueCalc(temp2 * cMAC + xMAC + 0.25 * cMAC)


###################################################################################################
# EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
