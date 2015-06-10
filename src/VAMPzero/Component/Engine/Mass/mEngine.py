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
from math import e

from VAMPzero.Handler.Parameter import parameter


class mEngine(parameter):
    '''
    The power unit mass definition equals the Airbus weight chapter 20 to 26. The power unit mass 
    includes: engines, nacelles, all systems included in the 
    removable power plant, and residual fluids hydraulic, 
    trapped fuel and oil in lines (not oil in tanks). Also included are aircraft systems 
    associated with engines: engine controls, bleed air and fuel systems. In detail it is broken down as follows:
    
    * equipped engines (complete removable power plant; w/o engine tank oil and electrical generators oil)
    
       * basic engine in manufacturer delivery configuration
       * nacelle structure (inlet cowls, fan cowls, nozzles, centerbody, reversers and engine mounts, ex-ternal paint final coat)
       * nacelle systems (all systems located within the nacelle)
    
    * bleed air system (in pylons, wing and fuselage)
    * engine control system (in pylons, wing and fuselage)
    * fuel system (incl. pipes, couplings, removable brackets, control and monitoring equipment, semi-equipment and their installations; excl. cables, electrical control and monitoring items)
    * inert gas system (incl. inert gas generation, storage, distribution, generation control and generation indicating systems)
    
    The system masses exclude fittings on which they are fixed but include the bolds that are used for fixing the systems.
    
    The mass definition between the Airbus accounting and the DIN 9020 
    (which is normally used within LTH) differs in several points. Differing with 
    the Airbus accounting the DIN 9020 group *propulsion* includes:
    
    * the tank sealant
    * unusable fuel in tanks
    
    and excludes: 
    
    * the engine nacelle structure and engine nacelle systems
    * the bleed air system

	
    :Unit: [kg]
    '''

    def __init__(self, value=0., unit='kg', parent='', cpacsPath=''):
        super(mEngine, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)


    def calc(self):
        '''
        Calculates the engine's mass based on the takeoff thrust and number of engines. 
        
        :Source: LTH UL-442.0(T). 
        '''
        self.setDeviation(0.074) # needs to be set by the calc method when called for later use (deviation depends on the calc method)
                
        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        thrustTOISA = self.parent.aircraft.engine.thrustTOISA.getValue()
        return self.setValueCalc(nEngine * 0.2953 * (thrustTOISA) ** 0.8063)

    def calcDiameter(self):
        '''
        Calculates the engine's mass based on the number of engines and their diameter.

        :Source: Analyse des Standes der Technik und Prognose von Entwicklungstrends im Triebwerkssektor, J. Grundmann, IB-328-2013-14, 2013, p. 65, eq. 50
        '''

        nEngine = self.parent.aircraft.engine.nEngine.getValue()
        dEngine = self.parent.dEngine.getValue()

        return self.setValueCalc(nEngine * (1.59 * dEngine*1000.-147.))

    def calcDorbath(self):
        '''
        Calculates the engine's mass based on the takeoff thrust the bypass ratio and the number of engines
        
        .. deprecated:: 0.3
        
            Use the LTH formulas instead
        
        :Source: Improvements on a Very Simple Preliminary Aircraft Design Model, F. Dorbath, Airbus FPO, 2008, p.140
        '''

        thrustTOISA = self.parent.aircraft.engine.thrustTOISA.getValue()
        bPR = self.parent.bypassRatio.getValue()
        n = self.parent.nEngine.getValue()

        return self.setValueCalc(14.7 * (thrustTOISA / 1000.) ** 1.1 * e ** (-0.045 * bPR) * n)

        ###################################################################################################
        #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
