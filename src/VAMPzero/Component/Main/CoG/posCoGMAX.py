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
import time
import numpy as np                      
from VAMPzero.Handler.Parameter import parameter

class posCoGMAX(parameter):
    '''
    The maximum x position of the center of gravity of the aircraft.
    It is calculated considering different combinations of fuel and payload.
    
    :Unit: [m]
    
    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(posCoGMAX, self).__init__(value=value, unit='m', doc=self.__doc__, status='init', parent=parent,
                                     cpacsPath=cpacsPath)

        # need to initialize a few values as elsewise they hinder the first iteration
        self.posCoG_fuel =[10.]
        self.m_PAX = [10.]
        self.posCoGMIN_fuel_pay0 = [10.]
        self.posCoGMIN_fuel_pay = [10.]
        self.posCoGMAX_fuel_pay0 = [10.]
        self.posCoGMAX_fuel_pay = [10.]
        self.m_TOW_fuel_pay = [10.]

    def createWeightAndBalance(self):
        '''
        Calculates the position-matrix of the center of gravity for different tank and PAX combinations.
        '''
        #Maximum Take Off Mass and maximum fuel weight
        mTOM = self.parent.mTOM.getValue()
        mTOM = mTOM.real

        #Length of cockpit and cabin
        lcockpit = self.parent.fuselage.lcockpit.getValue()
        lcabin = self.parent.fuselage.lcabin.getValue()
        
        #Operational Empty Mass and moment of oEM
        oEM = self.parent.oEM.getValue()
        oEM = oEM.real
        MoEM = self.parent.posCoGOEM.getValue() * oEM       

        # max allowable added weight
        maxLoad = mTOM - oEM

        #Cargo mass and moment
        mCargo = self.parent.payload.mCargo.getValue()
        MCargo = self.parent.fuselage.posCoG.getValue() * mCargo
        
        #Fuel mass and moment of the fuel  
        mfuelMAXCWT = self.parent.fuel.mFuelMAXcenterWT.getValue()
        mfuelMAXIWT = self.parent.fuel.mFuelMAXinnerWT.getValue()
        mfuelMAXOWT = self.parent.fuel.mFuelMAXouterWT.getValue()
        mfuelMAXTT = self.parent.fuel.mFuelMAXTT.getValue()
        
        posCoGCWT = self.parent.fuel.posCoGcenterWT.getValue()
        posCoGIWT = self.parent.fuel.posCoGinnerWT.getValue()
        posCoGOWT = self.parent.fuel.posCoGouterWT.getValue()
        posCoGTT = self.parent.fuel.posCoGTT.getValue()

        #Payload (single load of a PAX, number of PAX per row, number of all rows in the A/C)
        mSinglePax = self.parent.payload.mSinglePax.getValue()
        nPaxR = int(self.parent.fuselage.nPaxR.getValue())
        nRow = int(self.parent.fuselage.nRow.getValue())
        xPitch = lcabin/nRow
        nPaxRodd = nPaxR % 2            #modulo calculation for consideration several aircraft with an odd number of seats in one row, e.g. 9 abreast

        nLoadCases = int(nRow*(nPaxR/2+nPaxR % 2))
        nLoads = nPaxR/2

        # Passenger loading
        # The seat matrix marks the location of each passenger row
        seatMatrix = lcockpit + np.arange(nRow)*xPitch

        # The load matrix specifies how many passengers are seated in each row
        # We seat all A seats before all B seats etc.
        paxMatrix = np.tri(nLoadCases, nRow)*2.
        for i in range(nLoads-1):
            nextLoad = np.tri(nLoadCases-(i+1)*nRow, nRow)*2.
            zero = np.zeros((nRow*(i+1), nRow))
            paxMatrix = paxMatrix + np.vstack((zero, nextLoad))

        # Repeat for uneven configurations
        if nPaxRodd > 0.:
            i +=1
            nextLoad = np.tri(nLoadCases-(i+1)*nRow, nRow)
            zero = np.zeros((nRow*(i+1), nRow))
            paxMatrix = paxMatrix + np.vstack((zero, nextLoad))

        # Add a first 'unloaded' row
        paxMatrix = np.vstack((np.zeros(nRow), paxMatrix))

        frontToBack = paxMatrix*mSinglePax
        backToFront = np.fliplr(frontToBack)

        # Fuel loading
        nTanks = 4

        # similar to seatMatrix, the posCoG of the tanks from outer to inner
        tankCoG = [posCoGOWT, posCoGIWT, posCoGCWT, posCoGTT]
        maxFuel = [mfuelMAXOWT, mfuelMAXIWT, mfuelMAXCWT, mfuelMAXTT]

        tankMatrix = np.vstack((np.zeros(nTanks), np.tri(nTanks, nTanks)))
        for i in range(nLoadCases):
            tankMatrix = np.vstack((tankMatrix,np.zeros(nTanks), np.tri(nTanks, nTanks)))

        fuelMatrix = tankMatrix * maxFuel

        # This gives us a a max load matrix. Each pax Load Case combined with each fuel load case
        # Note that this matrix may still exceed max load
        #
        # At first tanking scheme from outer wing tank to center wing tank will be explored
        # As for each passenger loading step the passenger mass is the same there is no need to split these steps
        frontToBack_OutToCenter = np.hstack((np.repeat(frontToBack, nTanks+1, axis=0), fuelMatrix))
        backToFront_OutToCenter = np.hstack((np.repeat(backToFront, nTanks+1, axis=0), fuelMatrix))

        for i in np.where(frontToBack_OutToCenter.sum(axis=1)>maxLoad)[0]:
            for j in range(nTanks): # Go through all tanks and unload them until mTOM is satisfied
                if frontToBack_OutToCenter[i,:].sum()-maxLoad <= 0.: # If maxLoad is not exceeded anymore stop the loop
                    break
                elif frontToBack_OutToCenter[i,:].sum()-maxLoad > maxFuel[j]:
                    frontToBack_OutToCenter[i,nRow+j] = 0.
                    backToFront_OutToCenter[i,nRow+j] = 0.
                else:
                    frontToBack_OutToCenter[i,nRow+j] = frontToBack_OutToCenter[i,nRow+j] - (frontToBack_OutToCenter[i,:].sum()-maxLoad)
                    backToFront_OutToCenter[i,nRow+j] = backToFront_OutToCenter[i,nRow+j] - (backToFront_OutToCenter[i,:].sum()-maxLoad)


        # Now the opposite loading scheme for the tanks
        frontToBack_CenterToOut = np.hstack((np.repeat(frontToBack, nTanks+1, axis=0), fuelMatrix))
        backToFront_CenterToOut = np.hstack((np.repeat(backToFront, nTanks+1, axis=0), fuelMatrix))

        nTotal = nRow + nTanks - 1

        for i in np.where(frontToBack_CenterToOut.sum(axis=1)>maxLoad)[0]:
            for j in range(nTanks): # Go through all tanks and unload them until mTOM is satisfied
                if frontToBack_CenterToOut[i,:].sum()-maxLoad <= 0.:
                    break
                elif frontToBack_CenterToOut[i,:].sum()-maxLoad > maxFuel[-(j+1)]:
                    frontToBack_CenterToOut[i,nTotal-j] = 0.
                    backToFront_CenterToOut[i,nTotal-j] = 0.
                else:
                    frontToBack_CenterToOut[i,nTotal-j] = frontToBack_CenterToOut[i,nTotal-j] - (frontToBack_CenterToOut[i,:].sum()-maxLoad)
                    backToFront_CenterToOut[i,nTotal-j] = backToFront_CenterToOut[i,nTotal-j] - (backToFront_CenterToOut[i,:].sum()-maxLoad)

        leverMatrix = np.hstack((seatMatrix, tankCoG))

        #Matrix of the take-off mass (consider PAX and fuel) for both refueling orders.
        tow = oEM + mCargo + frontToBack_CenterToOut.sum(axis=1)

        cog_frontToBack_OutToCenter = (MoEM+np.dot(frontToBack_OutToCenter, leverMatrix)+MCargo)/tow
        cog_frontToBack_CenterToOut = (MoEM+np.dot(frontToBack_CenterToOut, leverMatrix)+MCargo)/tow
        cog_backToFront_OutToCenter = (MoEM+np.dot(backToFront_OutToCenter, leverMatrix)+MCargo)/tow
        cog_backToFront_CenterToOut = (MoEM+np.dot(backToFront_CenterToOut, leverMatrix)+MCargo)/tow

        cog_min = np.hstack((cog_backToFront_CenterToOut, cog_backToFront_OutToCenter))
        cog_max = np.hstack((cog_frontToBack_CenterToOut, cog_frontToBack_OutToCenter))

        self.posCoGMIN_fuel_pay0 = cog_min
        self.posCoGMIN_fuel_pay  = cog_min

        self.posCoGMAX_fuel_pay0 = cog_max
        self.posCoGMAX_fuel_pay  = cog_max

        self.m_TOW_fuel_pay = np.hstack((tow,tow))


    def calc(self):
        '''
        Calculates the maximum x location for the overall center of gravity for the aircraft.
        '''
        self.createWeightAndBalance()

        #maximum value of all CoG positions (payload and fuel)
        maxPosCoG = self.posCoGMAX_fuel_pay0.max()

        return self.setValueCalc(maxPosCoG)
