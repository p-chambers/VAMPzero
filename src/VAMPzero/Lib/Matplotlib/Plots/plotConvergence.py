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
from VAMPzero.Lib.Matplotlib.matplotlib import saveFigure

def plotConvergence(myAircraft):
                
    fig = figure(figsize=(15,15))
    ax  = axes()
    myAircraft.plotter(ax)
#    leg = ax.legend(loc='upper right',frameon=False,ncol=5)
#    for t in leg.get_texts():
#        t.set_fontsize('xx-small')

    
    ax.tick_params(pad=10,labelsize='x-large')
    ax.set_xscale('log')
    ax.grid(True, which='both', ls='-')
    ylabel('rel. Change [-]',size='40')        
    xlabel('Iteration [-]',size='40')
    saveFigure('Convergence')
    close(fig) 

