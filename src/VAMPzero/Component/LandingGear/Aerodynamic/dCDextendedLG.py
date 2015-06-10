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


class dCDextendedLG(parameter):
    '''
    The delta in the total drag coefficient of the aircraft due an extended landing gear
    
    :Unit: []
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(dCDextendedLG, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                            cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the drag increase due to extended landing gear
        
        :Source: Flugzeugentwurf I, Vorlesung, V. Gollnick
        '''

        mTOM = self.parent.aircraft.mTOM.getValue()
        mLG = self.parent.mLandingGear.getValue()
        refArea = self.parent.aircraft.wing.refArea.getValue()

        if mTOM <= 100000.:
            corr = 0.00093
        else:
            corr = 0.00157

        return self.setValueCalc(corr * mLG ** 0.73 / refArea)
