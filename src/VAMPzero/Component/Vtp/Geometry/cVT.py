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


class cVT(parameter):
    '''
    The vertical tail volume coefficient 
    
    :Unit: [ ] 
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(cVT, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                  cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the vertical tail volume coefficient
        cHT is derived from the T/W Ratio, sizing for engine failure 
        
        :Source: Ermittlung der Leitwerksflaechen im Flugzeugvorentwurf unter Einsatz des Fallbasierten Schliessens, S. Balluff, J. Pfaff, S. Rudolph, R. Voit-Nitschmann, DLRK, 2009, p.6
        '''
        self.setDeviation(0.193) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
        
        T = self.parent.aircraft.engine.thrustTO.getValue()
        mTOM = self.parent.aircraft.mTOM.getValue()
        n = self.parent.aircraft.engine.nEngine.getValue()

        return self.setValueCalc(T / (mTOM * 9.81) * n / 4.)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################