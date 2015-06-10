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
        dfus = self.parent.dfus.getValue()
        lfus = self.parent.lfus.getValue()

        f = lfus / dfus
        
        # limit the form factor to values between 0 and 2 for stability of convergence
        formFactor = 1 + 60. / f ** 3 + f / 400.
        if formFactor < 0.0:
            self.log.warning("VAMPzero AERO: The fuselages form factor is calculated to be less than 0.0. Resetting the value to 0.0.")
            formFactor = 0.0
        elif formFactor > 2.0:
            self.log.warning("VAMPzero AERO: The fuselages form factor is calculated to be more than 2.0. Resetting the value to 2.0.")
            formFactor = 2.0

        return self.setValueCalc(formFactor)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################