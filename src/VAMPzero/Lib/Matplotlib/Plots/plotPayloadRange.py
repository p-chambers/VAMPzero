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

from pylab import *
from VAMPzero.Lib.Colors.colors import zeroColor, giveColorForNetworkx

#Get the Colors from central location! Corporate Design ftw!
aircraftC       = zeroColor["aircraft"]
wingC           = zeroColor["wing"]
fuselageC       = zeroColor["fuselage"]
engineC         = zeroColor["engine"]
atmosphereC     = zeroColor["atmosphere"]
vtpC            = zeroColor["vtp"]
htpC            = zeroColor["htp"] 
fuelC           = zeroColor["fuel"] 
systemsC        = zeroColor["systems"]
airfoilC        = zeroColor["airfoil"]
pylonC          = zeroColor["pylon"]
landingGearC    = zeroColor["landingGear"]
payloadC        = zeroColor["payload"]

def plotPayloadRange(myAircraft):
    '''
    Is used to generate a Paylaod Range Diagramm of the Aircraft configuration
    should not be triggered unless VAMPzero has already reached convergence
    '''
    myAircraft.log.info("VAMPzero PLOT: Calculation PayloadRange Diagram")
    myAircraft.log.info("VAMPzero PLOT: .. this will trigger three calcAuto runs")
    
    fig = figure(figsize=(15,15))
    ax  = axes()
    x = []
    y = []
    z = []
    v = []
    l = []

    
    myAircraft.freeze()
    myAircraft.desRange.setStatus("calc")
    myAircraft.distCR.setStatus("calc")
    myAircraft.distCLIMB.setStatus("calc")
    myAircraft.distDESCENT.setStatus("calc")
    myAircraft.distRES.setStatus("calc")

    myAircraft.timeCR.setStatus("calc")
    myAircraft.timeCLIMB.setStatus("calc")
    myAircraft.timeDESCENT.setStatus("calc")
    myAircraft.timeRES.setStatus("calc")

    myAircraft.fuel.mFuelCR.setStatus("calc")
    myAircraft.fuel.mFuelCLIMB.setStatus("calc")
    myAircraft.fuel.mFuelDESCENT.setStatus("calc")
    myAircraft.fuel.mFuelRES.setStatus("calc")

    mPayloadTemp    = [myAircraft.payload.mPayload.getValue()]*2
    mZFWTemp        = [myAircraft.mZFW.getValue()]*2
    mTOMTemp        = [myAircraft.mTOM.getValue()]*2
    mTOM            = myAircraft.mTOM.getValue()
    oEM             = myAircraft.oEM.getValue()
    mLMTemp         = [myAircraft.mLM.getValue()]*2
    mFuelMAXTemp    = [myAircraft.fuel.mFuelMAX.getValue()]*2
    
    

    ax.plot([myAircraft.desRange.getValue()/1000.,myAircraft.desRange.getValue()/1000.],[0.,mTOM],'k-.',label='designPoint')

    ################################################################################################################
    #Point 0 maximum Payload fill up with no fuel
    ################################################################################################################
    

    x.append(0.)
    y.append(myAircraft.payload.mPayload.getValue())
    z.append(0.)
    
    v.append(myAircraft.payload.mPayload.getValue()+oEM)#+myAircraft.fuel.mFM.getValue()#)
    l.append(myAircraft.payload.mPayload.getValue()+oEM)
    
    ################################################################################################################
    #Point 1 maximum Payload fill up with fuel!
    #Set mission Fuel Mass to the highest value without exceeding mTOM
    ################################################################################################################
    if mTOM- oEM- myAircraft.payload.mPayload.getValue() < myAircraft.fuel.mFuelMAX.getValue():
        myAircraft.fuel.mFM.setValueFix(mTOM- oEM- myAircraft.payload.mPayload.getValue())
    else:
        myAircraft.log.debug("VAMPzero PLOT: Payload Failure Can not Reach maximum Fuel Mass")
        myAircraft.fuel.mFM.setValueFix(myAircraft.fuel.mFuelMAX.getValue())
        
    myAircraft.calcAuto()
    

    x.append(myAircraft.desRange.getValue()/1000.)
    y.append(myAircraft.payload.mPayload.getValue())
    z.append(myAircraft.fuel.mFM.getValue())

    v.append(myAircraft.fuel.mFM.getValue()+myAircraft.payload.mPayload.getValue()+oEM)
    l.append(myAircraft.payload.mPayload.getValue()+oEM)    
    
    ################################################################################################################    
    #Point 2 maximum Fuel in Tanks Rest Payload
    #Only adjust Payload if it is less then mTOM minus max Fuel and oEM
    ################################################################################################################
    
    addWeight  = mTOM - oEM
    maxFuel    = myAircraft.fuel.mFuelMAX.getValue()
    
    if maxFuel >= addWeight:
        myAircraft.fuel.mFM.setValueFix(addWeight)
        myAircraft.payload.mPayload.setValueFix(0.)
    else:
        myAircraft.fuel.mFM.setValueFix(maxFuel)
        myAircraft.payload.mPayload.setValueFix(addWeight-maxFuel)

    myAircraft.calcAuto()
    
    x.append(myAircraft.desRange.getValue()/1000.)
    y.append(myAircraft.payload.mPayload.getValue())
    z.append(myAircraft.fuel.mFM.getValue())

    v.append(myAircraft.fuel.mFM.getValue()+myAircraft.payload.mPayload.getValue()+oEM)    
    l.append(myAircraft.payload.mPayload.getValue()+oEM)        

    ################################################################################################################
    #Point 3 maximum Fuel in Tanks no Payload
    ################################################################################################################
    
    myAircraft.payload.mPayload.setValueFix(0.)
    myAircraft.calcAuto()


    x.append(myAircraft.desRange.getValue()/1000.)
    y.append(myAircraft.payload.mPayload.getValue())
    z.append(myAircraft.fuel.mFM.getValue())
    
    v.append(myAircraft.fuel.mFM.getValue()+myAircraft.payload.mPayload.getValue()+oEM)    
    l.append(myAircraft.payload.mPayload.getValue()+oEM)

    ################################################################################################################
    #Do the Plotting
    ################################################################################################################
    ax.plot(x,v,'o-',color=giveColorForNetworkx(aircraftC),label='actual TakeOff Mass')

    ax.plot(x,z,'o-',color=giveColorForNetworkx(fuelC),label='mission Fuel Mass')
    
    ax.plot(x,l,'o-',color=giveColorForNetworkx(wingC),label='actual Landing Mass')
    
    ax.plot(x,y,'o-',color=giveColorForNetworkx(payloadC),label='carried Payload Mass')

    ax.plot([0.,myAircraft.desRange.getValue()/1000.],mZFWTemp,'--',color=giveColorForNetworkx(engineC),label='maximum Zero Fuel Mass')

    ax.plot([0.,myAircraft.desRange.getValue()/1000.],mPayloadTemp,color=giveColorForNetworkx(payloadC),linestyle='--',label='design Payload Mass')
    
    ax.plot([0.,myAircraft.desRange.getValue()/1000.],mTOMTemp,'--',color=giveColorForNetworkx(aircraftC),label='maximum TakeOff Mass')

    ax.plot([0.,myAircraft.desRange.getValue()/1000.],mLMTemp,'--',color=giveColorForNetworkx(wingC),label='maximum Landing Mass')
    
    ax.plot([0.,myAircraft.desRange.getValue()/1000.],mFuelMAXTemp,color=giveColorForNetworkx(fuelC),linestyle='--',label='maximum Fuel Mass')
    
    ################################################################################################################       
    xlabel('Range [km]')
    ylabel('Mass [kg]')
    grid(False)
    leg = ax.legend(loc='center left',frameon=False)
    for t in leg.get_texts():
        t.set_fontsize('small')      
    title('VAMPzero PayloadRange ',color=(139/255.,0,0))
    fig.savefig('./ReturnDirectory/payloadRange.pdf')
    close(fig)
    
    ################################################################################################################
    #Write the points of the payload range diagram to a file
    ################################################################################################################
    points = zip(x,y)
    PR_outfile = './ReturnDirectory/PRpoints.csv'
    with open(PR_outfile,'w') as outfile:
        cases = []
        outfile.write('Range0;Payload0;RangeA;PayloadA;RangeB;PayloadB;RangeC;PayloadC\n')
        for p in points:
            cases.append("%f;%f" %(p))
        outfile.write(';'.join(cases) + '\n')

