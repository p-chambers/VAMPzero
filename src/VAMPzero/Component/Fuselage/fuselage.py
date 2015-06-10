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

from VAMPzero.Component.Fuselage.Aerodynamic.cD0c import cD0c
from VAMPzero.Component.Fuselage.Aerodynamic.cfLAM import cfLAM
from VAMPzero.Component.Fuselage.Aerodynamic.cfTURB import cfTURB
from VAMPzero.Component.Fuselage.Aerodynamic.dragArea import dragArea
from VAMPzero.Component.Fuselage.Aerodynamic.formFactor import formFactor
from VAMPzero.Component.Fuselage.Aerodynamic.nLam import nLam
from VAMPzero.Component.Fuselage.Aerodynamic.reynoldsNr import reynoldsNr
from VAMPzero.Component.Fuselage.Cabin.cargoDeck import cargoDeck
from VAMPzero.Component.Fuselage.Cabin.nAisle import nAisle
from VAMPzero.Component.Fuselage.Cabin.nClasses import nClasses
from VAMPzero.Component.Fuselage.Cabin.nPaxR import nPaxR
from VAMPzero.Component.Fuselage.Cabin.nRow import nRow
from VAMPzero.Component.Fuselage.Cabin.refAbreast import refAbreast
from VAMPzero.Component.Fuselage.Cabin.refLayout import refLayout
from VAMPzero.Component.Fuselage.CoG.posCoG import posCoG
from VAMPzero.Component.Fuselage.Geometry.xRoot import xRoot
from VAMPzero.Component.Fuselage.Geometry.LoD import LoD
from VAMPzero.Component.Fuselage.Geometry.dfus import dfus
from VAMPzero.Component.Fuselage.Geometry.lcabin import lcabin
from VAMPzero.Component.Fuselage.Geometry.lcockpit import lcockpit
from VAMPzero.Component.Fuselage.Geometry.lfus import lfus
from VAMPzero.Component.Fuselage.Geometry.lnose import lnose
from VAMPzero.Component.Fuselage.Geometry.loverlay import loverlay
from VAMPzero.Component.Fuselage.Geometry.ltail import ltail
from VAMPzero.Component.Fuselage.Geometry.wetArea import wetArea
from VAMPzero.Component.Fuselage.Mass.mFurn import mFurn
from VAMPzero.Component.Fuselage.Mass.mFuselage import mFuselage
from VAMPzero.Component.Fuselage.Mass.mStructure import mStructure
from VAMPzero.Handler.Component import component
from VAMPzero.Lib.CPACS.Export.Fuselage.fuselage import createFuselageProfile, \
    createFuselage
from VAMPzero.Component.Fuselage.Cabin.paxDensity import paxDensity
from VAMPzero.Component.Fuselage.Cabin.yFloor import yFloor
from VAMPzero.Component.Fuselage.Cabin.zFloor import zFloor
from VAMPzero.Component.Fuselage.Cabin.vcabin import vcabin
from VAMPzero.Component.Fuselage.Cabin.hcabin import hcabin
from VAMPzero.Component.Fuselage.Cabin.dcabin import dcabin


class fuselage(component):
    '''
    fuselage Class
    '''

    def __init__(self, aircraft):
        '''
        initializes fuselage object
        mostly used for documentation
        establishes link to the aircraft class
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'fuselage'
        self.aircraft = aircraft
        self.level = 2

        #Mass
        self.mFuselage = mFuselage()
        self.mFurn = mFurn(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mFurnishing/massDescription/mass')
        self.mStructure = mStructure(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mFuselagesStructure/mFuselageStructure/massDescription/mass')

        #CoG
        self.posCoG = posCoG(
            cpacsPath='/cpacs/vehicles/aircraft/model/analyses/massBreakdown/mOEM/mEM/mStructure/mFuselagesStructure/mFuselageStructure/massDescription/location/x')

        #Geometry
        self.xRoot = xRoot()# the fuselages origin
        self.dfus = dfus()
        self.lfus = lfus()#cpacsPath='/cpacs/toolspecific/joeFuMo/lfuselage')
        self.lcabin = lcabin()#cpacsPath='/cpacs/toolspecific/joeFuMo/deck/length')
        self.lcockpit = lcockpit()
        self.lnose = lnose()#cpacsPath='/cpacs/toolspecific/joeFuMo/lnose')
        self.ltail = ltail()#cpacsPath='/cpacs/toolspecific/joeFuMo/ltail')
        self.loverlay = loverlay()#cpacsPath='/cpacs/toolspecific/joeFuMo/loverlay')
        self.wetArea = wetArea()
        self.LoD = LoD()

        #Cabin
        self.nRow = nRow()
        self.nPaxR = nPaxR()
        self.nAisle = nAisle()
        self.nClasses = nClasses()
        self.refLayout = refLayout()#cpacsPath='/cpacs/toolspecific/joeFuMo/deck/refLayout',)
        self.refAbreast = refAbreast()#cpacsPath='/cpacs/toolspecific/joeFuMo/deck/refAbreast',)
        self.cargoDeck = cargoDeck()#cpacsPath='/cpacs/toolspecific/joeFuMo/cargoDeck')
        self.paxDensity = paxDensity()
        self.dcabin = dcabin()
        self.hcabin = hcabin()
        self.vcabin = vcabin()
        self.yFloor = yFloor()
        self.zFloor = zFloor()

        #Aerodynamics
        self.formFactor = formFactor()
        self.reynoldsNr = reynoldsNr()
        self.cfLAM = cfLAM()
        self.cfTURB = cfTURB()
        self.cD0c = cD0c()
        self.dragArea = dragArea()
        self.nLam = nLam()

    ###################################################################################################
    ##Export to CPACS
    ###################################################################################################

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        cpacsPath must be filled
        '''
        # level of detail
        self.log.debug("lfus,lcabin,lcockpit,lnose,ltail,loverlay: %s, %s, %s, %s, %s, %s" % (
            self.lfus.getValue(), self.lcabin.getValue(), self.lcockpit.getValue(), self.lnose.getValue(),
            self.ltail.getValue(), self.loverlay.getValue()))
        createFuselageProfile(CPACSObj, 'Circle')
        createFuselage(CPACSObj, self.id, self.dfus.getValue(), self.lnose.getValue(),
                       self.lfus.getValue() - self.ltail.getValue() - self.lnose.getValue(), self.ltail.getValue(),
                       self.LoD.getValue())

        super(fuselage, self).cpacsExport(CPACSObj)

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
        
