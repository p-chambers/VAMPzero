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
from cmath import pi

class cLROLL(parameter):
    '''
    The airplanes CL for the Take Off during rolling.
    
    :Unit: [ ]  
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cLROLL, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                    cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the airplanes CL for the Take Off during rolling.
        
        :Source: Bruening, Hafer, Sachs: Flugleistungen: Grundlagen, Flugzustaende, Flugabschnitte, 1993, vol. 2, p. 291
        
        :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''
        aspectRatio = self.parent.wing.aspectRatio.getValue()
        oswald = self.parent.wing.oswald.getValue()
        mu = 0.025
        
        
        cLROLL = pi * aspectRatio * oswald * mu/2

        return self.setValueCalc(cLROLL)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################