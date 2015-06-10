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
from math import sqrt, pi, asin

from VAMPzero.Handler.Parameter import parameter

rad = pi / 180.


class phi25(parameter):
    '''
    The sweep angle of the strut at the 25% chord line. Currently, there are
    two simplifications included in the strut model:

    * The strut is not tapered and hence all sweep angles are identical
    * This parameter may be set as user input.
      All other sweep angles of the strut read their values from here

    The angle of sweep which characterizes a swept wing is
    conventionally measured along the 25% chord line. If 
    the 25% chord line varies in sweep angle, the leading edge is used; 
    if that varies, the sweep is expressed in sections (e.g., 25 degrees 
    from 0 to 50% span, 15 degrees from 50% to wingtip).

    :Unit: [deg]
    :Wiki: http://en.wikipedia.org/wiki/Swept_wing
    '''

    def __init__(self, value=0., unit='deg', parent='', cpacsPath=''):
        super(phi25, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Set the sweep angle to zero as a default value.  Note that this will be beneficial for
        the structural aspects as it enables the strut to take the bending moments easily.
        Nevertheless, this may result in penalties for the aerodynamics, especially for wave drag.
        '''
        return self.setValueCalc(0.)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################