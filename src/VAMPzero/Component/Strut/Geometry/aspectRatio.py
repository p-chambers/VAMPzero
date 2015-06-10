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


class aspectRatio(parameter):
    '''
    In aerodynamics, the aspect ratio of a wing is essentially the ratio of its length to its breadth (chord). 
    A high aspect ratio indicates long, narrow wings, whereas a low aspect ratio indicates short, stubby wings.
    For most wings the length of the chord is not a a constant but varies along the wing, so the aspect ratio AR 
    is defined as the square of the wingspan b divided by the area refArea of the wing planform - this is equal to 
    the length-to-breadth ratio for constant breadth.

    This parameter describes the aspectRatio for the strut. Currently, the taperRatio of the strut is assumes to
    equal one, hence only simple calculations are included here.
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Aspect_ratio_(wing) 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(aspectRatio, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        Standard definition of the aspect ratio
        '''
        span = self.parent.span.getValue()
        area = self.parent.refArea.getValue()
        return self.setValueCalc(span ** 2 / area)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################