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
from __future__ import division
from VAMPzero.Handler.Parameter import parameter


class reynoldsNr(parameter):
    '''
    In fluid mechanics, the Reynolds number Re is a dimensionless number 
    that gives a measure of the ratio of inertial forces to viscous forces 
    and consequently quantifies the relative importance of these two types 
    of forces for given flow conditions.    
    
    :Unit: [ ]
    :Wiki: http://en.wikipedia.org/wiki/Reynolds_number   
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(reynoldsNr, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                         cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reynoldsnumber relative to the 
        wing's mean aerodynamic chord length for the cruise true air speed
        
        :Source: me
        '''
        ny = self.parent.aircraft.atmosphere.nyCR.getValue()
        TAS = self.parent.aircraft.atmosphere.TASCR.getValue()
        cMAC = self.parent.cMAC.getValue()

        return self.setValueCalc(TAS * cMAC / ny)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################