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
from cmath import pi, tan

from VAMPzero.Handler.Parameter import parameter


rad = pi / 180.


class xEngine(parameter):
    '''
    X-location of the engine inlet
	
    :Unit: [m]
    '''

    def __init__(self, value=0., unit='m', parent='', cpacsPath=''):
        super(xEngine, self).__init__(value=value, unit=unit, doc=self.__doc__, status='init', parent=parent,
                                      cpacsPath=cpacsPath)

    def calcChortAtEta(self, eta, phiLE, phiTE, cRoot, etaKink, span, yFuselage):
        """
        todo::
           This is a copy of the function in flap.py maybe need to shift this somewhere else
        """
        # if eta lies at the fuselage than return cRoot
        if eta <= yFuselage / span / 2.:
            return cRoot
        
        # elif eta lies in the inboard section return cRoot minus the bit lost due to leading edge sweep angle
        elif eta <= etaKink:
            l = span / 2.*eta - yFuselage
            cFront = l / tan(((90 - phiLE)) * rad)
            return cRoot - cFront
        
        # elif eta lies in the outboard section return cRoot minus the bit lost due to leading edge sweep angle + the bit gained due to the trailingedge angle
        elif eta > etaKink and eta < 1.:
            l1 = span / 2.*eta - yFuselage
            l2 = span / 2.*eta - span / 2.* etaKink
            cFront = l1 / tan(((90 - phiLE) * rad))
            cBack = l2 / tan(((90 - phiTE) * rad))
            return cRoot - cFront + cBack
        else:
            self.log.warning('VAMPzero CHORD: Calculation of chord at eta location called for invalid eta: %s' % str(eta))
            raise ValueError

    def calc(self):
        '''
        Calculates the X-location of the engine depending on the location value.
        If the location value of the engine is equal to 1, engine is wing mounted.
        else engine is fuselage mounted.

        '''


        location = self.parent.location.getValue()
        if location == 1.:
            self.calc = self.calcWingMount
        else:
            self.calc = self.calcFuselageMount



    def calcWingMount(self):
        '''
        Calculates the X-location of the engine for the wing mounted engines from the engines diameter and the
        wing position. It is assumed that the engine is located underneath the wing.
        
        The calculation follows the picture from Stanfords online course, but does apply some simplifications: 
        
        * As location x/c is chosen to be -0.1; h/c is taken for the easy curve and therefore should be ~ -0.09
        * The end of the outer flow is chosen to be at 0.65% of overall engine length
        * As no curvature information for the nacelle is available h is parallel to the engine axis
        * values are relative to the leading edge of the wing 

        :Source: http://adg.stanford.edu/aa241/propulsion/engineplacement.html
        '''

        yEngine = self.parent.yEngine.getValue()
        span = self.parent.aircraft.wing.span.getValue()
        eta = self.parent.aircraft.wing.etaEngine.getValue()
        phiLE = self.parent.aircraft.wing.phiLE.getValue()
        phiTE = self.parent.aircraft.wing.phiTE.getValue()
        cRoot = self.parent.aircraft.wing.cRoot.getValue()
        etaKink = self.parent.aircraft.wing.etaKink.getValue()
        yFuselage = self.parent.aircraft.wing.yFuselage.getValue()
        

        # The engine is positioned relative to the leading edge. At first the x position
        # of the leading edge at the engine location is determined
        xRoot = self.parent.aircraft.wing.xRoot.getValue()
        l = yEngine - yFuselage
        cFront = l / tan(((90. - phiLE)) * rad)
        dX = xRoot + cFront
        
        # the inlet of the engine is furthermore located xOverC to the front. and an additional 0.66 of engine length are added
        xOverC = -0.1
        c = self.calcChortAtEta(eta, phiLE, phiTE, cRoot, etaKink, span, yFuselage) 
        lEngine = self.parent.lEngine.getValue()
        
        dX = dX + xOverC * c - 0.66 * lEngine  

        return self.setValueCalc(dX)


    def calcFuselageMount(self):
        '''
        Calculates the X-location of the engine for the fuselage mounted engines from the engine length and the
        fuselage length.

        The calculation follows the picture from Stanfords online course, and taken similar to Fokker 100:

        * The end of the outer flow is chosen to be at 0.65% of overall engine length
        * The end of the outer cowl is assumed to be at 82% of the fuselage length.

        :Source: http://www.fokker-aircraft.info/f100general.htm
        :Source: http://adg.stanford.edu/aa241/propulsion/engineplacement.html
        '''

        lEngine = self.parent.lEngine.getValue()
        lFuselage = self.parent.aircraft.fuselage.lfus.getValue()
        xRootFuselage = self.parent.aircraft.fuselage.xRoot.getValue() # consider a possible translation of the fuselage
        # The end of the outer cowl is assumed to be at 82% of the fuselage length.


        return self.setValueCalc(0.82*lFuselage - 0.66 * lEngine + xRootFuselage)

        ###################################################################################################
        # EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
        ###################################################################################################
