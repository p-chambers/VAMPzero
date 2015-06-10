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
from cmath import pi, tan, sqrt

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class expArea(parameter):
    '''
    The exposed area of the wing
    
    :Unit: [m2] 
    :Wiki: http://adg.stanford.edu/aa241/wingdesign/winggeometry.html
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(expArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the exposed Area by subtracting a trapezoid from the reference area
        The trapezoid has the lengths a = cRoot, c = cInter, where cInter is the chord at the fuselage/wing intersection
        and h = yfus, where yfus is the y coordinate of the wing/fuselage intersection  
        '''
        refArea = self.parent.refArea.getValue()
        cRoot = self.parent.cRoot.getValue()
        cTip = self.parent.cTip.getValue()
        span = self.parent.span.getValue()/2.
        dfus = self.parent.aircraft.fuselage.dfus.getValue()
        zRoot = self.parent.zRoot.getValue()

        # calculate the y position of the wing fuselage intersection
        yfus = sqrt(dfus ** 2 / 4. - zRoot ** 2)

        cInter = cRoot + (cTip - cRoot)/(span)*(yfus)

        # remaining area is the referenceArea mins the trapezoid from croot, cinter and h = yfus
        result = refArea - ((cRoot + cInter) / 2 * yfus) * 2.

        return self.setValueCalc(result)

        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
