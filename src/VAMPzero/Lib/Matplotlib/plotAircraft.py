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


from VAMPzero.Lib.Matplotlib.Plots.plotConvergence import plotConvergence
from VAMPzero.Lib.Matplotlib.Plots.plotDrag import plotDrag
from VAMPzero.Lib.Matplotlib.Plots.plotGeometry import plotGeometry
from VAMPzero.Lib.Matplotlib.Plots.plotMFUEL import plotMFUEL
from VAMPzero.Lib.Matplotlib.Plots.plotMTOM import plotMTOM
from VAMPzero.Lib.Matplotlib.Plots.plotOEM import plotOEM
from VAMPzero.Lib.Matplotlib.Plots.plotPayloadRange import plotPayloadRange
from VAMPzero.Lib.Matplotlib.Plots.plotDOC import plotDOC
from VAMPzero.Lib.Matplotlib.Plots.plotCOC import plotCOC

def plotAircraft(myAircraft):
    '''
    calls other plotting subroutines
    '''
            
    myAircraft.log.info('')
    myAircraft.log.info("##############################################################################")
    myAircraft.log.info("VAMPzero Plotting")
    myAircraft.log.info("creating visualization in ReturnDirectory")
    myAircraft.log.info("##############################################################################")
    
    
    plotGeometry(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: Geometry done.")

    plotMTOM(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: MTOM cake done.")

    plotMFUEL(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: MFUEL cake done.")

    plotOEM(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: OEM cake done.")

    plotConvergence(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: Convergence history done.")

    plotDrag(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: Component drag cake done.")

    plotDOC(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: DOC cake done.")
    
    plotCOC(myAircraft)
    myAircraft.log.debug("VAMPzero PLOT: COC cake done.")

    plotPayloadRange(myAircraft)
    myAircraft.log.info("VAMPzero PLOT: Payloadrange done.")
    
    myAircraft.log.info("VAMPzero PLOT: done.")
    