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


class wsL(parameter):
    '''
    The wing loading for the landing
    
    In aerodynamics, wing loading is the loaded weight of the aircraft divided 
    by the area of the wing. The faster an aircraft flies, the more lift is produced 
    by each unit area of wing, so a smaller wing can carry the same weight in 
    level flight, operating at a higher wing loading. Correspondingly, the landing 
    and take-off speeds will be higher. The high wing loading also decreases 
    maneuverability. The same constraints apply to birds and bats.
    
    :Unit: [kg/m2]
    :Wiki: http://en.wikipedia.org/wiki/Wing_loading 
    '''

    def __init__(self, value=0., unit='kg/m2', parent='', cpacsPath=''):
        super(wsL, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        chooses the appropriate calculation method for the area loading at landing
        depending on the status of the landing field length
        
        If the status of sLFL is set to fix calcSizing will be called
        else calcWsTO is called
        '''
        sLFLstatus = self.parent.sLFL.getStatus()

        if sLFLstatus == "fix":
            self.calc = self.calcSizing
        else:
            self.calc = self.calcWsL

    def calcWsL(self):
        '''
        Calculates the wing loading for landing from the wing loading for take-off and the airplane masses
        
        :Source: Airplane Design Part I, J. Roskam, DARCorporation, 2005, Fourth Edition, p. 113
        '''
        mTOM = self.parent.mTOM.getValue()
        mLM = self.parent.mLM.getValue()
        wsTO = self.parent.wsTO.getValue()

        return self.setValueCalc(wsTO * mLM / mTOM)


    def calcSizing(self):
        '''
        Calculates the wing loading for landing condition from the wing loading for take-off and the landing mass
        
        :Source: Airplane Design Part I, J. Roskam, DARCorporation, 2005, Fourth Edition, p. 113
        '''
        sLFL = self.parent.sLFL.getValue()
        CLmaxL = self.parent.cLL.getValue()
        rhoAP = self.parent.atmosphere.rhoAP.getValue()

        #Calculate the Approach Speed eq 3.16. 0,3 has to be corrected by 0.3048 / 0.5144**2 
        Va = (sLFL / 0.345569) ** 0.5

        #Calculate the Landing Speed
        #@note: for fly by wire aircraft this value may be 1.23
        Vsl = Va / 1.3

        #Get the Wing Loading
        return self.setValueCalc(Vsl ** 2 * CLmaxL * rhoAP / 2 / 9.81)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################