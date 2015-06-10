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

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from VAMPzero.Lib.Colors.colors import giveColorForNetworkx, zeroColor
#from Lib.NetworkX.networkX import chooseColor


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


def plotSensitivityBar(name='nameOfTheParameter', names='namesOfAllDependingParameters', ups=None):
    '''
    Plots a sensitivity Bar
    @param name: Name of the Parameter used for saving as well 
    @param names: Namelist of dependent callees
    @param ups: upper sensitivity values
    '''
    if not os.path.exists('./ReturnDirectory/mindMaps/barPlots/'):
        os.makedirs('./ReturnDirectory/mindMaps/barPlots/')

    if ups:
        ind = np.arange(len(ups))
        fig = plt.figure(dpi=600, figsize=(9, len(names)))
        ax = plt.axes(frameon=False, xticks=[], yticks=[])

        for i, u, n in zip(ind, ups, names):
            c = chooseColor(n)
            ax.barh(i, u, facecolor='none', align='center', left=0., height=.5, edgecolor=c, linewidth=2.)

        rects = [rect for rect in ax.get_children() if isinstance(rect, Rectangle)]
        for rect, n, u in zip(rects, names, ups):
            width = int(rect.get_width())
            c = chooseColor(n)
            if u > 0.:
                xloc = 0.98*width
                align = 'right'
            else:
                xloc = -0.98*width
                align = 'left'

            yloc = rect.get_y()+rect.get_height()/2.0
            ax.text(xloc, yloc, n, horizontalalignment=align,
                    verticalalignment='center', color=c, weight='bold')

        ax.plot([0., 0.], [0, len(ups) - 1], 'k', alpha=0.25, linewidth=2.)
        ax.set_xticklabels([''])
        ax.set_yticklabels([''])

        plt.savefig('./ReturnDirectory/mindMaps/barPlots/' + name + '.png')
        plt.close(fig)


def plotSensitivityBarDoc(parameter, names, ups, calcName):
    '''
    Plots a sensitivity Bar for the documentation
    @param name: Name of the Parameter used for saving as well 
    @param names: Namelist of dependent callees
    @param ups: upper sensitivity values
    '''
    componentName = parameter.parent.id
    disciplineName = parameter["discipline"]
    name = parameter["name"]

    lName = parameter.longName.replace('.', '')
    fileName = parameter.picName
    #==============================================================================
    #Create Folder and File 
    #==============================================================================
    dir = os.path.dirname(fileName)
    if not os.path.exists(dir):
        os.makedirs(dir)

    if ups:
        ind = np.arange(float(len(ups)))
        fig = plt.figure(figsize=(4, len(ups) / 2.))
        ax = fig.add_subplot(111, axisbg='grey', frameon=False, xticks=[], yticks=[])

        colors = []
        values = []
        for item in ups:
            if item > 0.:
                color = giveColorForNetworkx(aircraftC)
            else:
                color = giveColorForNetworkx(engineC)

            colors.append(color)
            values.append(abs(item))

        ax.barh(ind, values, color=colors, align='center', left=0., height=.5, edgecolor='w')

        for Cname in names:
            ax.text(0, names.index(Cname), ' ' + Cname, ha='left', va='center', color='k', alpha=0.8, size=16)

        ax.plot([0., 0.], [-0.25, len(ups) -1 + .25], 'k', alpha=0.25, linewidth=2.)
        ax.set_xticklabels([''])
        ax.set_yticklabels([''])

        ax.set_title('')
        plt.savefig(fileName, dpi=300)
        plt.close(fig)


###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################        
