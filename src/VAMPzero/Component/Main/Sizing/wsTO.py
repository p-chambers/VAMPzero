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


class wsTO(parameter):
    '''
    The wing loading for take-off
    
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
        super(wsTO, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                   cpacsPath=cpacsPath)

    def calc(self):
        '''
        chooses the appropriate calculation method for the wing loading at take-off
        depending on the status of the landing field length
        
        If the landing field length is fixed the calcwsL method will be called
        else calcmTOM will be called
        '''
        sLFLstatus = self.parent.sLFL.getStatus()

        if sLFLstatus == "fix":
            self.calc = self.calcwsL
        else:
            self.calc = self.calcmTOM


    def calcmTOM(self):
        '''
        Calculates the wing loading for take-off from the area and max take-off mass
        
        .. todo::
        
           missing source
        '''
        mTOM = self.parent.mTOM.getValue()
        refArea = self.parent.wing.refArea.getValue()

        return self.setValueCalc(mTOM / refArea)


    def calcwsL(self):
        '''
        Calculates the wing loading for take-off from the wing loading for landing and the airplane masses
        
        :Source: Airplane Design Part I, J. Roskam, DARCorporation, 2005, Fourth Edition, p. 113
        '''
        mTOM = self.parent.mTOM.getValue()
        mLM = self.parent.mLM.getValue()
        WSl = self.parent.wsL.getValue()

        return self.setValueCalc(WSl * mTOM / mLM)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################