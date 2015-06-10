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


class refArea(parameter):
    '''
    The reference area of the struts, i.e. summed up for right and left strut.
    
    :Unit: [m2]
    :Wiki: http://adg.stanford.edu/aa241/wingdesign/winggeometry.html
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refArea, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reference area for the strut. Note that this is not the
        projected area of the strut. It takes into account the root chord lenght and
        the span of the strut.

        The calculation is only valid if the strut is not tapered.
        '''
        cRoot = self.parent.cRoot.getValue()
        span = self.parent.span.getValue()

        return self.setValueCalc(span * cRoot * 2)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################