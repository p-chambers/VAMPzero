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


class twTO(parameter):
    '''
    The thrust to weight ratio for take-off
    
    :Unit: [kg/m2]
    :Wiki: http://en.wikipedia.org/wiki/Thrust-to-weight_ratio
    '''

    def __init__(self, value=0., unit='kg/m2', parent='', cpacsPath=''):
        super(twTO, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        chooses the appropriate calculation method for the thrust to weight ratio at take-off
        depending on the status of the take-off field length
        
        If the take-off field length is fixed the method calcsTOFL is chosen
        else the method calcThrustTO is chosen
        '''
        thrustTOstatus = self.parent.engine.thrustTO.getStatus()

        if thrustTOstatus == "fix":
            self.calc = self.calcThrustTO
        else:
            self.calc = self.calcTWmax


    def calcThrustTO(self):
        '''
        Calculates the thrust to weight ratio at take-off
        assuming that take-off thrust is given per engine
        
        .. todo::
        
           missing source
        '''
        nEngine = self.parent.engine.nEngine.getValue()
        mTOM = self.parent.mTOM.getValue()
        thrustTO = self.parent.engine.thrustTO.getValue()

        return self.setValueCalc(nEngine * thrustTO / (mTOM * 9.81))

    def calcTWmax(self):
        '''
        Calculates the thrust to weight setting at takeoff for the maximum required
        
        Depending on the status of the takeoff field lenght the twTOP25 requirement is taken into
        account or not.  
        '''
        sTOFLstatus = self.parent.sTOFL.getStatus()

        twFAR25121a = round(self.parent.twFAR20121a.getValue(), 3)
        twFAR25121b = round(self.parent.twFAR20121b.getValue(), 3)
        twTOP25 = round(self.parent.twTOP25.getValue(), 3)

        if sTOFLstatus == 'fix':
            return self.setValueCalc(max([twFAR25121a, twFAR25121b, twTOP25]))
        else:
            return self.setValueCalc(max([twFAR25121a, twFAR25121b]))

            ###################################################################################################
            #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
            ###################################################################################################