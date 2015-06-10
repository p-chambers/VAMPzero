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


def plotDrag(myAircraft):
    # make a square figure and axes
    fig         = figure(figsize=(15,15))
    ax          = axes([0.1, 0.1, 0.8, 0.8])
    
    labels      = []
    fracs       = []
    colors      = []
    
    labels.append(myAircraft.wing.id)
    fracs.append(myAircraft.wing.cD0c.getValue())
    colors.append(giveColorForNetworkx(wingC))


    labels.append(myAircraft.htp.id)
    fracs.append(myAircraft.htp.cD0c.getValue())
    colors.append(giveColorForNetworkx(htpC))


    labels.append(myAircraft.vtp.id)
    fracs.append(myAircraft.vtp.cD0c.getValue())
    colors.append(giveColorForNetworkx(vtpC))
    
    labels.append(myAircraft.fuselage.id)
    fracs.append(myAircraft.fuselage.cD0c.getValue())
    colors.append(giveColorForNetworkx(fuselageC))

    
    labels.append(myAircraft.engine.id)
    fracs.append(myAircraft.engine.cD0c.getValue())
    colors.append(giveColorForNetworkx(engineC))

    
    explode=[0.05]*len(labels)
    
    
    myPie = pie(fracs, explode=explode,labels=labels,colors=colors, autopct='%1.1f%%', shadow=True)
    
    legends = []
    for i in range(len(fracs)):
        out = '%-10s= %.2f'%(labels[i],fracs[i])
        legends.append(out)  
    
    ax.legend(myPie[0],legends,shadow = True)
    
    saveFigure('Component Drag')
    close(fig)