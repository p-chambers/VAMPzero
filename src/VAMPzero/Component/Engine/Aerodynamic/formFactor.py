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


class formFactor(parameter):
    '''
    The parasite drag associated with skin friction and pressure drag is determined 
    by incrementing the flat plate results by a factor, to account for 
    pressure drag and the higher-than-freestream surface velocities:

    :Unit: [ ]
    :Wiki: http://adg.stanford.edu/aa241/drag/formfactor.html	
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(formFactor, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the form factor for the engine from length and diameter

        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.  283, Eq. 12.32
        '''
        dEngine = self.parent.dEngine.getValue()
        lEngine = self.parent.lEngine.getValue()

        if dEngine != 0. and lEngine != 0.:
            return self.setValueCalc(1 + 0.35 / (lEngine / dEngine))


            ###################################################################################################
            #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
            ###################################################################################################