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


class cMAC(parameter):
    '''
    Physically, MAC is the chord of a rectangular wing, which has the same area, 
    aerodynamic force and position of the center of pressure at a given angle of attack as 
    the given wing has. Simply stated, MAC is the width of an equivalent rectangular wing in given 
    conditions. Therefore, not only the measure but also the position of MAC is often important. 
    In particular, the position of center of mass (CoM) of an aircraft is usually measured relative to the 
    MAC, as the percentage of the distance from the leading edge of MAC to CoM with respect to MAC itself.    
    
    :Unit: [m]
    :Wiki: http://en.wikipedia.org/wiki/Chord_(aircraft)#Mean_aerodynamic_chord
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(cMAC, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the wing mean aerodynamic chord
        
        :Source: Aircraft Design: A Conceptual Approach, D. P. Raymer, AIAA Education Series, 1992, Second Edition, p.49
        '''
        self.setDeviation(0.0544) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        taperRatio = self.parent.taperRatio.getValue()
        cRoot = self.parent.cRoot.getValue()

        return self.setValueCalc(2 / 3. * cRoot * (1 + taperRatio + taperRatio ** 2) / (1 + taperRatio))

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################