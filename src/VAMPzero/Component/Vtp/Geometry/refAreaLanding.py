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
from cmath import sqrt, pi, cos, tan, atan

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.TIXI.tixi import openTIXI, checkElement
from VAMPzero.Lib.TIGL.tigl import openTIGL, getWingSurfaceArea


class refAreaLanding(parameter):
    '''
    The reference area for the vertical tailplane for the Take Off.
    
    :Unit: [m2]

    :Author: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
    '''

    def __init__(self, value=0., unit='m2', parent='', cpacsPath=''):
        super(refAreaLanding, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calc(self):
        '''
        Calculates the reference area for the VTP from the moment of equilibrium as a result of a cross wind landing. The VTP has to compensate the
        cross wind during the landing process. Therefore the rudder deflection has to be less than the maximum value. Here the VTP area can't calculated in a
        direct way, because the area dissapear in the following equations. Therefore the required rudder deflection for compensating the cross wind has to 
        be calculated in order to give a warning in case of non-fulfillment.
        
        :Source: Patrick Goden, Technische Universitaet Hamburg Harburg, Master Thesis
        '''   
        aAP = self.parent.aircraft.atmosphere.aAP.getValue()
        aspectRatioVPT = self.parent.aspectRatio.getValue()
        phi50VTP = self.parent.phi50.getValue()
        refAreaVTP = self.parent.refAreaTakeOff.getValue()
        wsL = self.parent.aircraft.wsL.getValue()
        cLL = self.parent.aircraft.cLL.getValue()
        rhoAP = self.parent.aircraft.atmosphere.rhoAP.getValue()

        #Stall speed Calculation
        vL = sqrt(2 * wsL * 9.81 / (rhoAP * cLL))*1.2 #Eq. 3.1 from Roskam I p-90
        machL = vL/aAP
        max_crosswind = 30.         #in[kn]
        zeta_req = 25               #in [deg], maximum value
        c_Q_beta_profile = 6.1416   #in [1/rad], for the VTP profile
        C_Q_zeta = 1.0616           #in [1/rad]

        kappaVTP = c_Q_beta_profile * (1 - machL**2)/(2 * pi)
        C_Q_beta = (2 * pi * aspectRatioVPT)/(2 + sqrt(aspectRatioVPT**2/kappaVTP**2 * (tan(phi50VTP*pi/180)**2 + 1 - machL**2) + 4)) #in [1/rad], for the VTP wing

        beta_req = (max_crosswind*(1.852/3.6)/vL)*180/pi

        zeta = (C_Q_beta/C_Q_zeta) * beta_req    # in [deg]
        zeta = zeta.real

        if zeta > zeta_req:
            self.log.debug('VAMPzero CALC: Crosswind landing is not possible under present conditions!')

        return self.setValueCalc(refAreaVTP)   # the crosswind landing is just an estimation of the needed VTP with no calculated HTP at the end, so the HTP from the take off
                            # case is used
