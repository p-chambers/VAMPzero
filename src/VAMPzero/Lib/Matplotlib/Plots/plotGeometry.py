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
from __future__ import division

from mpl_toolkits.mplot3d.axes3d import Axes3D
from pylab import *

from VAMPzero.Lib.Colors.colors import zeroColor, giveColorForNetworkx
from VAMPzero.Lib.Matplotlib.matplotlib import saveFigure


rad = pi / 180.

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


def plotWingGeom(ax, myWing, style = [91.,91.,91.]):
    xRoot       = myWing.xRoot.getValue()
    zRoot       = myWing.zRoot.getValue()
    cRoot       = myWing.cRoot.getValue()
    cTip        = myWing.cTip.getValue()
    phiLE       = myWing.phiLE.getValue()
    span        = myWing.span.getValue()
    
    xMAC        = myWing.xMAC.getValue()
    yMAC        = myWing.yMAC.getValue()
    cMAC        = myWing.cMAC.getValue()

    xMAC        = (xMAC,xMAC+cMAC)    
    yMAC        = (yMAC,yMAC)
    zMAC        = (0.,0.)
    ax.plot(xMAC, yMAC, zMAC,color=giveColorForNetworkx(style),linestyle='--')
    
    xw          = (xRoot,xRoot+span/2.*tan(phiLE*rad),xRoot+span/2.*tan(phiLE*rad)+cTip,xRoot+cRoot,xRoot)
    yw          = (0.,span/2.,span/2.,0.,0.)
    zw          = (zRoot,zRoot,zRoot,zRoot,zRoot)
    ax.plot(xw, yw, zw, label=myWing.id,color=giveColorForNetworkx(style))

    xw          = (xRoot+0.25*cRoot,xRoot+0.25*cTip+span/2.*tan(phiLE*rad))
    yw          = (0.,span/2.)
    zw          = (zRoot,zRoot)
    ax.plot(xw, yw, zw,color=giveColorForNetworkx(style),linestyle='--')
    
    return ax

def plotWingHighGeom(ax, myWing, style = [91.,91.,91.]):
    def plotLine(ax,style, x,y,z,c):
        x = (x,x+c)
        y = (y,y)
        z = (z,z)
        ax.plot(x, y, z,color=giveColorForNetworkx(style),linestyle='--')
        return ax
    
    xRoot           = myWing.xRoot.getValue()
    zRoot           = myWing.zRoot.getValue()
    cRoot           = myWing.cRoot.getValue()

    xFuselage       = myWing.xFuselage.getValue()
    yFuselage       = myWing.yFuselage.getValue()
    zFuselage       = myWing.zFuselage.getValue()
    cFuselage       = myWing.cFuselage.getValue()

    xKink           = myWing.xKink.getValue()
    yKink           = myWing.yKink.getValue()
    zKink           = myWing.zKink.getValue()
    cKink           = myWing.cKink.getValue()

    xTip            = myWing.xTip.getValue()
    zTip            = myWing.zTip.getValue()
    cTip            = myWing.cTip.getValue()
    
    span            = myWing.span.getValue() /2.
    
    ax              = plotLine(ax, style, xRoot, 0., zRoot, cRoot)
    ax              = plotLine(ax, style, xFuselage, yFuselage, zFuselage, cFuselage)
    ax              = plotLine(ax, style, xKink, yKink, zKink, cKink)
    ax              = plotLine(ax, style, xTip, span, zTip, cTip)
    
    return ax

def plotVtpGeom(ax, myWing, style = [91.,91.,91.]):
    xRoot       = myWing.xRoot.getValue()
    zRoot       = myWing.zRoot.getValue()
    cRoot       = myWing.cRoot.getValue()
    cTip        = myWing.cTip.getValue()
    phiLE       = myWing.phiLE.getValue()
    span        = myWing.span.getValue()
    
    xMAC        = myWing.xMAC.getValue()
    yMAC        = myWing.yMAC.getValue()
    cMAC        = myWing.cMAC.getValue()

    xMAC        = (xMAC,xMAC+cMAC)    
    zMAC        = (yMAC,yMAC)
    yMAC        = (0.,0.)
    ax.plot(xMAC, yMAC, zMAC, color=giveColorForNetworkx(style),linestyle='--')
    
    xw          = (xRoot,xRoot+span*tan(phiLE*rad),xRoot+span*tan(phiLE*rad)+cTip,xRoot+cRoot,xRoot)
    zw          = (zRoot,zRoot+span,zRoot+span,zRoot,zRoot)
    yw          = (0.,0.,0.,0.,0.)
    ax.plot(xw, yw, zw, label=myWing.id,color=giveColorForNetworkx(style))

    xw          = (xRoot+0.25*cRoot,xRoot+0.25*cTip+span*tan(phiLE*rad))
    zw          = (zRoot,zRoot+span)
    yw          = (0.,0.)
    ax.plot(xw, yw, zw, color=giveColorForNetworkx(style),linestyle='--')
    
    return ax

def cRooteateCylinder(start,length,diameter):
    #first Circle
    x   = []
    y   = []
    z   = []
    n   = 30
    
    #First HalfCircle
    for i in range(n):
        x.append(start)
        y.append(diameter/2.*sin(i/n*180*rad)) 
        z.append(diameter/2.*cos(i/n*180*rad))
    
    #Straight Lines
    x.extend([start,start+length,start+length,start,start])
    y.extend([0.,0.,0.,0.,0.])
    z.extend([diameter/2.,diameter/2.,-diameter/2.,-diameter/2.,diameter/2.])
        
    for i in range(n):
        x.append(start+length)
        y.append(diameter/2.*sin(i/n*180*rad)) 
        z.append(diameter/2.*cos(i/n*180*rad))
    
    return tuple(x),tuple(y),tuple(z)

def plotFuselageGeom(ax,myFuselage, style = [91.,91.,91.]):

    
    dfus        = myFuselage.dfus.getValue()
    
    lcabin      = myFuselage.lcabin.getValue()
    ltail       = myFuselage.ltail.getValue()
    lnose       = myFuselage.lnose.getValue()
    loverlay       = myFuselage.loverlay.getValue()

    #Nose
    x,y,z       = cRooteateCylinder(0, lnose, dfus)
    ax.plot(x, y, z, color=giveColorForNetworkx(style),linestyle='--')
    
    #Cabin
    x,y,z       = cRooteateCylinder(lnose-(lnose-2.4),lcabin , dfus)
    ax.plot(x, y, z, label=myFuselage.id,color=giveColorForNetworkx(style))

    #Tail
    x,y,z       = cRooteateCylinder(lnose-(lnose-2.4)+lcabin-loverlay ,ltail, dfus)
    ax.plot(x, y, z, color=giveColorForNetworkx(style),linestyle='--')

    return ax

def plotEngineGeom(ax,myEngine,style = [91.,91.,91.]):
    lEngine     = myEngine.lEngine.getValue()
    dEngine     = myEngine.dEngine.getValue()
    xEngine     = myEngine.xEngine.getValue()
    yEngine     = myEngine.yEngine.getValue()
    
    x,y,z       = cRooteateCylinder(xEngine,lEngine,dEngine)
    ploty       = [value + yEngine for value in y]
    ax.plot(x, ploty, z, label=myEngine.id,color=giveColorForNetworkx(style))
    
    return ax

def plotCoG(ax,myAircraft,style = [91.,91.,91.]):
    coG  = myAircraft.posCoG.getValue()
    
    pos  = coG 
    ax.plot(tuple([pos]),tuple([0.]),tuple([0.]),'D', label='CoG',color='k',ms=10)
    
    return ax

def plotGeometry(myAircraft):

    fig         = figure(figsize=(15,15))
    ax          = Axes3D(fig)
        
    ax          = plotWingGeom(ax, myAircraft.wing,wingC)
    ax          = plotWingGeom(ax, myAircraft.htp,htpC)
    ax          = plotCoG(ax, myAircraft,engineC)
    #note: this is a high level representation of the wings geometry
    #ax          = plotWingHighGeom(ax, myAircraft.wing,fuelC)
    ax          = plotVtpGeom(ax, myAircraft.vtp,vtpC)
    ax          = plotFuselageGeom(ax, myAircraft.fuselage,fuselageC)
    ax          = plotEngineGeom(ax,myAircraft.engine,engineC)
    
    ax.set_xlim3d(0,myAircraft.fuselage.lfus.getValue()+2)
    ax.set_ylim3d(0,myAircraft.fuselage.lfus.getValue()+2)
    ax.set_zlim3d(0,myAircraft.fuselage.lfus.getValue()+2)
    ax.set_aspect('equal')

    leg = ax.legend(loc='right')
    for t in leg.get_texts():
        t.set_fontsize('small')  

    
    ax.view_init(elev=90.,azim=0.)
    saveFigure('aircraftGeomTop',True)

    ax.view_init(elev=0.,azim=90.)
    saveFigure('aircraftGeomSide',True)

    ax.set_xlim3d(0,myAircraft.wing.span.getValue()/2.+2)
    ax.set_ylim3d(0,myAircraft.wing.span.getValue()/2.+2)
    ax.set_zlim3d(0,myAircraft.wing.span.getValue()/2.+2)

    ax.view_init(elev=0.,azim=180.)
    saveFigure('aircraftGeomFront',True)
    close(fig)
    
    

    

    
    