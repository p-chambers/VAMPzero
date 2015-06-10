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


class distCR(parameter):
    '''
    The distance traveled during the cruise segment
    
    :Unit: [m] 
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(distCR, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

    def calc(self):
        '''
        Sets ths calc method for the calculation of the distance traveled in the cruise segment
        depending on the status of the design range. If the design range is fixed calcFixRange is chosen, 
        else calcFixFuel is chosen. 
        
        .. todo::
        
           catch error if both or none are fixed.
        '''
        if self.parent.desRange.getStatus() == 'fix':
            return self.calcFixRange()
        else:
            return self.calcFixFuel()

    def calcFixRange(self):
        '''
        Calculates the distance for the cruise segment if the range is given
        
        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''
        distCLIMB = self.parent.distCLIMB.getValue()
        distDESCENT = self.parent.distDESCENT.getValue()
        distRES = self.parent.distRES.getValue()
        desRange = self.parent.desRange.getValue()

        if desRange - distCLIMB - distDESCENT - distRES > 0.:
            return self.setValueCalc(desRange - distCLIMB - distDESCENT - distRES)
        else:
            self.log.error(
                'VAMPzero CALC: The mission is too short to calculate a distance traveled in the cruise segment!')
            return self.setValueCalc(desRange)

    def calcFixFuel(self):
        '''
        Calculates the distance for the cruise segment if the fuel for the segment is given
        
        :Source: adapted from DLR-LY-IL Performance Tool, J. Fuchte, 2011
        '''
        TAS = self.parent.atmosphere.TASCR.getValue()
        timeCR = self.parent.timeCR.getValue()

        return self.setValueCalc(TAS * timeCR)




        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################