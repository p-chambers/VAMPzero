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
import math

class costCrew(parameter):
    '''
    The crew costs per flight hour
    
    :Unit: [EU/hr]
    '''

    def __init__(self, value=0., unit='EU/hr', parent='', cpacsPath=''):
        super(costCrew, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                       cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates crew costs, method from TU Berlin

        :Source: TU Berlin - Simplified DOC model, J. Thorbeck (remarks by D. Scholz)
                http://www.fzt.haw-hamburg.de/pers/Scholz/Aero/TU-Berlin_DOC-Method_with_remarks_13-09-19.pdf
        '''
        paxSeats = self.parent.payload.paxSeats.getValue()                      # Number of passengers on aircraft [#]
        tFlight = self.parent.tFlight.getValue()                                # Flight time of one flight [hr]
        flightCycles = self.parent.flightCycles.getValue()                      # Number of flight cycles per year [#]
        
        # Values given in source
        
        salaryFA = 60000.0                                                      # Average salary flight attendants [EU/yr]
        salaryFC = 300000.0                                                     # Averay salary of cockpit crew [EU/yr]
        CC = 5.0                                                                # Crew complement [-]
        
        # Calculations

        # Need to insert a small workaround here to make it also work in complex mode
        try:
            nFA = math.ceil(paxSeats / 50)                                          # Number of flight attendants -> certification requirement
        except:
            nFA = math.ceil(paxSeats.real / 50)                                          # Number of flight attendants -> certification requirement

        costCrew = CC * (salaryFA * nFA + salaryFC) / (tFlight * flightCycles)
        
        return self.setValueCalc(costCrew)
        
    def calcQUICE(self):
        '''
        Calculates the crew cost per flight hour
        The calculation method stems from the QUICE project 
        
        :Source: Analyse und Vergleich von DOC-Modellen zur Etablierung eines gemeinsam genutzten Rechenmodells bei Airbus und Universitaeten, M. Weiss, 2008
        '''
        nPilot = self.parent.nPilot.getValue()
        nCabinCrew = self.parent.nCabinCrew.getValue()
        utilization = self.parent.utilization.getValue()
        flightTime = self.parent.tFlight.getValue()
        blockTime = self.parent.tBlock.getValue()

        #=======================================================================
        # Salaries
        #=======================================================================
        pilotSalary = 150000.       #Euro/year
        attendantSalary = 60000.        #Euro/year
        crewComplement = 5.            #Total number of Crews needed to operate the aircraft

        #=======================================================================
        # Pilots
        #=======================================================================
        costPilotAnnual = nPilot * pilotSalary
        costPilot = costPilotAnnual / (utilization / blockTime)

        #=======================================================================
        # Cabin Crew
        #=======================================================================
        costCabinAnnual = nCabinCrew * attendantSalary
        costCabin = costCabinAnnual / (utilization / blockTime)

        cost = (costCabin + costPilot) / flightTime * crewComplement
        return self.setValueCalc(cost)

    def calcEurocontrol(self):
        '''
        Calculates the crew costs per flight hour
        
        :Source: Dynamic Cost Indexing, Aircraft Crewing - marginal delay costs, EuroControl, 2008, p. 4, tab. 2
        '''
        nPilot = self.parent.nPilot.getValue()
        nCabinCrew = self.parent.nCabinCrew.getValue()

        #=======================================================================
        # Pilots
        #=======================================================================
        costPilot = 0.
        # Assuming medium range (A320) cost if not more than two pilots are operating the aircraft 
        if nPilot > 0:
            costPilot = 133.54
        if nPilot > 1:
            costPilot = 133.54 + 70.53
            # Assuming long range (B767) cost if not more than two pilots are operating the aircraft
        if nPilot > 2:
            costPilot = 2 * 186.82 + (nPilot - 2.) * 125.31

        #=======================================================================
        # Crew
        #=======================================================================
        costCabinCrew = 0.
        # One Senior
        if nCabinCrew > 0:
            costCabinCrew = 42.84
            # One Senior, one Attendant
        if nCabinCrew > 1:
            costCabinCrew = 42.84 + 28.51
            # One Senior, n-1 Attendants
        if nCabinCrew > 2:
            costCabinCrew = 1 * 42.84 + (nCabinCrew - 1) * 28.51
            # Two Senior, n-2 Attendants
        if nCabinCrew > 5:
            costCabinCrew = 2 * 42.84 + (nCabinCrew - 2) * 28.51
            # Three Senior, n-3 Attendants
        if nCabinCrew > 7:
            costCabinCrew = 3 * 42.84 + (nCabinCrew - 3) * 28.51

        cost = costPilot + costCabinCrew
        return self.setValueCalc(cost)

    ###################################################################################################
    #EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
    ###################################################################################################
