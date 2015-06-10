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


###################################################################################################
##VAMPzero Imports
###################################################################################################

from VAMPzero.Component.Main.aircraft import aircraft

 
#Create Global Object
myAircraft = aircraft()

#global data
myAircraft.desRange.setValueFix( 3273000.) 
myAircraft.payload.paxSeats.setValueFix( 150.)
myAircraft.payload.mSinglePax.setValueFix( 90.)
myAircraft.payload.mCargo.setValueFix( 5000.)
myAircraft.fuel.mFuelMAX.setValueFix( 18400)
myAircraft.loDLOI.setValueFix( 11.)
myAircraft.altCR.setValueFix( 10000.)
myAircraft.machCR.setValueFix( 0.76)
myAircraft.timeRES.setValueFix( 0.5)
myAircraft.sTOFL.setValueFix( 3291)
myAircraft.sLFL.setValueFix( 1945)
myAircraft.cD0.setValueFix( 0.019)


#wing data
myAircraft.wing.taperRatio.setValueFix( 0.246)
myAircraft.wing.xRoot.setValueFix( 12.)
myAircraft.wing.refArea.setValueFix( 122.4)
myAircraft.wing.phi25.setValueFix( 25.)
myAircraft.wing.airfoilr.tc.setValueFix( 0.15)
myAircraft.wing.airfoilt.tc.setValueFix( 0.11 )
#myAircraft.wing.oswald.setValueFix( 0.8)
myAircraft.wing.aspectRatio.setValueFix( 9.4)
#myAircraft.wing.span.setValueFix( 34.)

#htp data
myAircraft.htp.airfoilr.tc.setValueFix( 0.1)
myAircraft.htp.airfoilt.tc.setValueFix( 0.1)
myAircraft.htp.aspectRatio.setValueFix( 5.)
myAircraft.htp.taperRatio.setValueFix( 0.33)
myAircraft.htp.phi25.setValueFix( 28)
myAircraft.htp.refArea.setValueFix( 31.)

#vtp data
myAircraft.vtp.airfoilr.tc.setValueFix( 0.1)
myAircraft.vtp.airfoilt.tc.setValueFix( 0.1)
myAircraft.vtp.aspectRatio.setValueFix( 1.6)
myAircraft.vtp.taperRatio.setValueFix( 0.35)
myAircraft.vtp.phi25.setValueFix( 35)
myAircraft.vtp.refArea.setValueFix( 21.5)


##
### Engine Data - CFM56-5A1
##

myAircraft.engine.nEngine.setValueFix( 2.)
myAircraft.engine.bypassRatio.setValueFix( 6.)
myAircraft.engine.TET.setValueFix( 1500.)
myAircraft.engine.OPR.setValueFix( 31.3)
myAircraft.engine.etaFan.setValueFix( 0.91)
myAircraft.engine.etaCompr.setValueFix( 0.90)
myAircraft.engine.etaTurb.setValueFix( 0.91)
myAircraft.engine.etaProp.setFactor( 1.10)


#myAircraft.engine.sfcCR.cpacsImport(cpacsIn)
#myAircraft.engine.sfcCR.calc = myAircraft.engine.sfcCR.calcOverallEff
#myAircraft.engine.PriceEngine.calc = myAircraft.engine.PriceEngine.calcJenk



#transfer mission data to atmosphere
myAircraft.atmosphere.hCR.setValueFix(myAircraft.altCR.getValue())
myAircraft.atmosphere.MaCR.setValueFix(myAircraft.machCR.getValue())

myAircraft.calcAuto()
myAircraft.createDoc()




###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################

