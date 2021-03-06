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

from VAMPzero.Lib.Matplotlib.matplotlib import createFigure, saveFigure
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


def plotDOC(myAircraft):
    # make a square figure and axes
    fig         = figure(figsize=(15,15))
    ax          = axes([0.1,0.1,0.8,0.8])
   
    labels      = []
    fracs       = []
    colors      = []
    '''
    #===========================================================================
    # COC
    #===========================================================================
    labels.append('costCrew')
    fracs.append(myAircraft.costCrew.getValue())
    colors.append(giveColorForNetworkx(wingC))

    labels.append('costFuel')
    fracs.append(myAircraft.costFuel.getValue())
    colors.append(giveColorForNetworkx(wingC))
    
    labels.append('costMaintenance')
    fracs.append(myAircraft.costMaintenance.getValue())
    colors.append(giveColorForNetworkx(wingC))

    labels.append('costNavigation')
    fracs.append(myAircraft.costNavigation.getValue())
    colors.append(giveColorForNetworkx(wingC))

    labels.append('costLanding')
    fracs.append(myAircraft.costLanding.getValue())
    colors.append(giveColorForNetworkx(wingC))

    labels.append('costGround')
    fracs.append(myAircraft.costGround.getValue())
    colors.append(giveColorForNetworkx(wingC))

    #===========================================================================
    # COO
    #===========================================================================
    labels.append('costDepreciation')
    fracs.append(myAircraft.costDepreciation.getValue())
    colors.append(giveColorForNetworkx(aircraftC))

    labels.append('costInterest')
    fracs.append(myAircraft.costInterest.getValue())
    colors.append(giveColorForNetworkx(aircraftC))

    labels.append('costInsurance')
    fracs.append(myAircraft.costInsurance.getValue())
    colors.append(giveColorForNetworkx(aircraftC))
    '''
    #===========================================================================
    # TU Berlin DOC method
    #===========================================================================
    
    # C1 = costCrew + CostCap
    
    labels.append('costCrew')
    fracs.append(myAircraft.costCrew.getValue())
    colors.append(giveColorForNetworkx(wingC)) 

    labels.append('costCap')
    fracs.append(myAircraft.costCap.getValue())
    colors.append(giveColorForNetworkx(wingC))
    
    # C2 = costFuel + costLanding + costGround + costNavigation + costMaintenance
    
    labels.append('costFuel')
    fracs.append(myAircraft.costFuel.getValue())
    colors.append(giveColorForNetworkx(aircraftC))
    
    labels.append('costLanding')
    fracs.append(myAircraft.costLanding.getValue())
    colors.append(giveColorForNetworkx(aircraftC))

    labels.append('costGround')
    fracs.append(myAircraft.costGround.getValue())
    colors.append(giveColorForNetworkx(aircraftC))

    labels.append('costNavigation')
    fracs.append(myAircraft.costNavigation.getValue())
    colors.append(giveColorForNetworkx(aircraftC))
    
    labels.append('costMaintenance')
    fracs.append(myAircraft.costMaintenance.getValue())
    colors.append(giveColorForNetworkx(aircraftC))
    
    #===========================================================================
    # Plot
    #===========================================================================
    explode=[0.05]*len(labels)
    myPie = pie(fracs, explode=explode,labels=labels,colors=colors, autopct='%1.1f%%', shadow=True)
    
    legends = []
    for i in range(len(fracs)):
        out = '%-10s= %.2f[EU/bh]'%(labels[i],fracs[i])
        legends.append(out)  
    
    ax.legend(myPie[0],legends,shadow = True)
         
    saveFigure('DOC Breakdown')
    close(fig)