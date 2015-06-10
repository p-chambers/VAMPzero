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


class posCoG(parameter):
    '''
    X Position of the center of gravity of the combined fuel
	
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(posCoG, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the posCoG from the individual fuel tanks cog.
        The cog of each fuel tank will be assumed to be constant.
        '''
        mFuelCWT = self.parent.mFuelMAXcenterWT.getValue()
        posCWT = self.parent.posCoGcenterWT.getValue()
        mFuelIWT = self.parent.mFuelMAXinnerWT.getValue()
        posIWT = self.parent.posCoGinnerWT.getValue()
        mFuelOWT = self.parent.mFuelMAXouterWT.getValue()
        posOWT = self.parent.posCoGouterWT.getValue()
        mFuelTT = self.parent.mFuelMAXTT.getValue()
        posTT = self.parent.posCoGTT.getValue()
        num = posCWT * mFuelCWT + posIWT * mFuelIWT + posOWT * mFuelOWT + posTT * mFuelTT
        den = (mFuelCWT + mFuelIWT + mFuelOWT + mFuelTT)
        return self.setValueCalc(num / den)


        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################