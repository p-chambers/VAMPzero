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


class massIY(parameter):
    '''
    The mass moment of inertia along the y-axis 
    
    :Unit: 'kgm2'
    :Wiki: http://en.wikipedia.org/wiki/Moment_of_inertia
    '''

    def __init__(self, value=0., unit='kgm2', parent='', cpacsPath=''):
        super(massIY, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the aircrafts moment of inertia in reference to y axis

        :Source: Luftfahrttechnisches Handbuch, N.N., 2004, 40242-01
        '''
        lfus = self.parent.fuselage.lfus.getValue()
        mTOM = self.parent.mTOM.getValue()
        oEM = self.parent.oEM.getValue()
        mFM = self.parent.fuel.mFM.getValue()

        m1 = mFM / oEM
        m2 = mTOM / oEM

        ky1 = m1 + 0.2 * (m2 - 1)
        ky = -0.04 * ky1 + 0.21

        return self.setValueCalc(ky * ky * lfus * lfus * mTOM)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
        