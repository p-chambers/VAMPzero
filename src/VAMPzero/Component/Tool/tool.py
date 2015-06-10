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
from VAMPzero.Handler.Component import component
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath


class tool(component):
    '''
    Class to hold all Toolspecific Data
    '''

    def __init__(self, aircraft):
        '''
        will initialize instance mainly used for documentation
        links to the aircraft instance
        initiates the airfoil class
        @Method: Component Constructor
        '''
        component.__init__(self)
        self.id = 'tool'
        self.aircraft = aircraft
        self.level = 2

        #===============================================================================
        #Aircraft stuff 
        #===============================================================================
        self.aircraftName = parameter(cpacsPath='/cpacs/vehicles/aircraft/model/name', value='VAMPzero')
        self.aircraftDES = parameter(cpacsPath='/cpacs/vehicles/aircraft/model/description', value='VAMPzero')
        #commented out due to introduction of xMAC25
        #self.refX             = parameter(cpacsPath = '/cpacs/vehicles/aircraft/model/reference/point/x',value='0.0')
        self.refY = parameter(cpacsPath='/cpacs/vehicles/aircraft/model/reference/point/y', value='0.0')
        self.refZ = parameter(cpacsPath='/cpacs/vehicles/aircraft/model/reference/point/z', value='0.0')

        #=======================================================================
        # Lifting Line
        #=======================================================================
        self.liliname = parameter(cpacsPath='/cpacs/toolspecific/liftingLine/tool/name', value='LIFTING_LINE')
        self.liliversion = parameter(cpacsPath='/cpacs/toolspecific/liftingLine/tool/version', value='2.3.1')
        self.liliuID = parameter(cpacsPath='/cpacs/toolspecific/liftingLine/aircraftModelUID',
                                 value='A320modelID')#@todo: Model ID is not available at Time of Construction
        self.liliSpaneling = parameter(
            cpacsPath='/cpacs/toolspecific/liftingLine/toolParameters/wingPanelings/wingPaneling[1]/spanwise',
            value='5')
        self.liliCpaneling = parameter(
            cpacsPath='/cpacs/toolspecific/liftingLine/toolParameters/wingPanelings/wingPaneling[1]/chordwise',
            value='5')

        self.lilimode = parameter(cpacsPath='/cpacs/toolspecific/liftingLine/toolParameters/archiveMode', value='1')
        #self.lilipolars       = parameter(cpacsPath = '/cpacs/toolspecific/liftingLine/performanceMaps',value='')


        #=======================================================================
        #Header Information 
        #=======================================================================
        self.name = parameter(cpacsPath='/cpacs/header/name', value='Export from')
        self.creator = parameter(cpacsPath='/cpacs/header/creator', value='VAMPzero')
        self.timestamp = parameter(cpacsPath='/cpacs/header/timestamp', value='2010-12-31T12:00:00')
        self.version = parameter(cpacsPath='/cpacs/header/version', value='0.1')
        self.version = parameter(cpacsPath='/cpacs/header/cpacsVersion', value='2.0')

    def importer(self, path):
        pass

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports all parameters nested in the component. Nested Components will be called as well. 
        cpacsPath must be filled
        '''

        def exportVector(CPACSObj, cpacsPath, value):
            myVector = getObjfromXpath(CPACSObj, cpacsPath)
            myType = "vector"
            myVector.set_valueOf_(str(value))
            myVector.set_mapType(myType)

        exportVector(CPACSObj, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/machNumber',
                     self.aircraft.atmosphere.MaCR.getValue())
        exportVector(CPACSObj, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/angleOfAttack', '0;2;4')
        exportVector(CPACSObj, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/angleOfYaw', '0')
        exportVector(CPACSObj, '/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/reynoldsNumber',
                     self.aircraft.wing.reynoldsNr.getValue())
        self.lilipolint = parameter(cpacsPath='/cpacs/toolspecific/liftingLine/toolParameters/usePOLINT', value="false")

        super(tool, self).cpacsExport(CPACSObj)