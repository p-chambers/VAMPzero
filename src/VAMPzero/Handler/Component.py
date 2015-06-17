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
from sys import exit
import inspect

import matplotlib

from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.general import printFooter
from VAMPzero.Lib.Log.log import zeroLogger
from VAMPzero.Lib.TIGL.tigl import openTIGL
from VAMPzero.Lib.TIXI.tixi import openTIXI, closeXML, getText
from VAMPzero.Lib.Sphinx.createDisciplineDoc import createDisciplineDoc
from VAMPzero.Lib.Sphinx.createComponentDoc import createComponentDoc
from VAMPzero.Handler.Types import zeroComplex
from VAMPzero.Lib.GUI.gui import importGUI
from VAMPzero.Lib.Matplotlib.plotAircraft import plotAircraft
from VAMPzero.Handler.Exceptions import NotConvergingError
import VAMPzero.Lib.CPACS.Export.export as exportLib


class component(object):
    '''
    **Superclass for all Components**
    
    The class component is inherited by all other components in VAMPzero. It defines the methods 
    that can be used throughout the code.
    
    Most calls in this class are recursive and reflexive as they go through all nested components 
    and parameters. For example the calc method will call all nested calc methods. 
    
    * If the member is a parameter, its calc is called
    
    * If the member is a component and the component is nested deeper in the call hierarchy its calc is called
    
    Additionally, an arbitrary number of disciplines can be defined to only call the respective calc methods.   
    
    .. note:: 
    
       disicplines are only known to the parameters in a component.
       
    Several other methods, for reporting, error handling and logging are located in component. See the respective methods documentation     
    '''

    def __init__(self):
        # Used for Logging Stuff
        self.log = zeroLogger('Component')

    # Access Parameters
    def getParameters(self, sorting=str.lower, componentWise=True):
        def getParametersOnly():
            params = []
            # go through all Parameters of self
            # distinguish between the two types parameter and component
            for para in sorted(self.__dict__, key=str.lower):
                para = getattr(self, para)
                # if paramter valid add to List
                if issubclass(para.__class__, parameter):
                    params.append(para)
            return params
        
        def getComponentsOnly():
            params = []
            for para in sorted(self.__dict__, key=str.lower):
                para = getattr(self, para)
                # if para is a subclass of component call the exporter again
                # check as well if para is of a lower level so that it will be called top down
                if issubclass(para.__class__, component) and para.level > self.level:
                    params.append(para)
            return params
        
        params = getParametersOnly()
        for comp in getComponentsOnly():
            params.extend(comp.getParameters(componentWise))
            
        if componentWise:
            return params
        return sorted(params, key=lambda para: para['name'].lower())
    
    # Report
    def report(self):
        '''
        Looking up init values for all Objects that are existent in the calculation modules
        If Parameter is a subclass of component inits will be called! 
        '''

        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero Report")
        self.log.info("displaying values of all parameters")
        self.log.info("##############################################################################")

        self.reporter()

        self.log.info("VAMPzero REPORT: done.")

    def reporter(self):
        '''
        recursive call for the report Method
        '''

        self.log.info('')
        self.log.info("VAMPzero REPORT: for component: %s" % self.id)
        # Go through all user declared attributes
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                para.realify()
                para.help()

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.reporter()

    def createMapping(self, fileHandler):
        '''
        @param fileHandler: to write mapping instructions
        '''
        self.log.info("VAMPzero MAP: for component: %s" % self.id)
        # Go through all user declared attributes
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter) and para.getCpacsPath() != '':
                cpacsPath = para.getCpacsPath()
                fileHandler.write("    <map:mapping mode=\"delete\" >\n")
                fileHandler.write("        <map:source>" + cpacsPath + "</map:source>\n")
                fileHandler.write("        <map:target>" + cpacsPath + "</map:target>\n")
                fileHandler.write("    </map:mapping>\n")
                self.log.debug("VAMPzero MAP: added item: %s to output mapping " % cpacsPath)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.createMapping(fileHandler)

    # Create Documentation
    def createDoc(self):
        '''
        will look up all adjacent cpacsPaths or checks if an own cpacsImport method was applied
        '''

        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero DOCU")
        self.log.info("building an aircraft and start creating documentation files")
        self.log.info("##############################################################################")

        self.documenter(self, parentFolder='./VAMPzero/doc/Components/')

        self.log.info("VAMPzero DOCU: done.")

    def documenter(self, myAircraft, parentFolder):
        '''
        recursive call for the createDoc method
        '''
        self.log.info('')
        self.log.info("VAMPzero DOCU: for component: %s" % self.id)

        parentFolder = parentFolder + self.id + '/'

        disciplines = {}
        components = []

        # Go through all user declared attributes 1
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is a parameter make him do his doc file
            if issubclass(para.__class__, parameter) and para["name"].find('uID') == -1:
                para.createDoc(myAircraft, parentFolder)

                if not para["discipline"] in disciplines:
                    disciplines[para["discipline"]] = []

                disciplines[para["discipline"]].append(para["name"])

            if issubclass(para.__class__, component) and para.level > self.level:
                if not para in components:
                    components.append(para)

        createDisciplineDoc(disciplines, parentFolder)
        createComponentDoc(self, self.__doc__, components, disciplines, parentFolder)

        # Go through all user declared attributes 2
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            #If para is component call documenter for this component
            if issubclass(para.__class__, component) and para.level > self.level:
                para.documenter(myAircraft, parentFolder)

    # Inits
    def inits(self):
        '''
        Looking up init values for all Objects that are existent in the calculation modules
        If Parameter is a subclass of component inits will be called! 
        '''

        def checkStatus(para):
            '''
            Checks whether the status of the parameter is init 
            '''

            if para.getStatus() == 'init':
                self.log.debug(
                    "    - %-*s is only initialized! Value is: %s" % (15, para.getName(), str(para.getValue())))

        # Inits Main
        self.log.debug('')
        self.log.debug("VAMPzero INIT: for component: %s" % self.id)
        # Go through all user declared attributes

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            #If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                checkStatus(para)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            #If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.inits()

    # Convergence
    def converge(self, converged):
        '''
        Validation of all Classes that are existent in the calculation modules
        All Parameters of Type List are checked of the Calculation Switch in entry [2]
        All Parameter of Type Aircraft are ignored
        If Parameter is a subclass of component validate will be called! 
        '''
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                if type(para.getValue()) == float or type(para.getValue()) == zeroComplex:
                    parameterConverged = para.checkConvergence()

                    #Case 1: a parameter has not converged
                    if not parameterConverged:
                        converged = False
                        #break

        # go on with checking
        if converged:
            for para in self.__dict__:
                para = getattr(self, para)

                #If para is component call yourself
                if issubclass(para.__class__, component) and para.level > self.level:
                    componentConverged = para.converge(converged)
                    if not componentConverged:
                        converged = False
                        #break

        if not converged:
            self.log.debug('VAMPzero CONV: At least one parameter/component in: %s did not converge' % self.id)
        elif converged:
            self.log.info('VAMPzero CONV: %-19s converged' % self.id)

        return converged

    # Freeze
    def freeze(self):
        '''
        Locking up fixed values for all Objects that are existent in the calculation modules
        If Parameter is a subclass of component freeze will be called!
        @todo: Enter possibility to lock only parameters of a certain discipline! 
        '''

        self.log.debug("VAMPzero FREEZE: for component: %s" % self.id)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            #If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                para.setStatus('fix')

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            #If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.freeze()

    # Complexify
    def complexify(self):
        '''
        This function goes thruogh all nested components and parameters and tries to complexify
        all parameters found to set them to type zeroComplex
        '''
        self.log.debug('')
        self.log.debug("VAMPzero COMPLEX: for component: %s" % self.id)

        # Go through all user declared attributes
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                para.complexify()

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.complexify()

    # Check inconsistencies
    def check(self):
        '''
        Looking up fixed values for all Objects that are existent in the calculation modules
        If a parameter is fixed and all callees as well throw a warning
        '''

        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero Check")
        self.log.info("looking for inconsistencies in the calculation")
        self.log.info("##############################################################################")

        self.checker()

        self.log.info("VAMPzero CHECK: done.")

    def checker(self):
        '''
        recursive method for finding all parameters with status FIX and examine their callees
        '''

        def isFix(para):
            '''
            Checks whether the status of the parameter is FIX 
            '''
            if para.getStatus() == 'fix':
                self.log.debug("    - %-*s is fixed! Value is: %s" % (15, para.getName(), str(para.getValue())))
                return True
            else:
                return False

        self.log.debug("VAMPzero FIX: for component: %s" % self.id)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter):

                if isFix(para):
                    ok = False
                    # go through all callees
                    for callee in para["callee"]:
                        # if the para is not fixed everything is fine
                        if not isFix(callee):
                            ok = True

                    if not ok and para["callee"] != []:
                        self.log.warning('VAMPzero CHECK: %s and all his callees are fixed!' % para.longName)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.checker()
    
    # Input Listings
    def inputs(self):
        '''
        Looking up fixed values for all Objects that are existent in the calculation modules
        If Parameter is a subclass of component inputs will be called! 
        '''

        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero Inputs")
        self.log.info("the following values are fixed and will not be altered!")
        self.log.info("##############################################################################")

        self.inputer()

        self.log.info("VAMPzero INPUTS: done.")

    def inputer(self):
        '''
        recursive method for finding all parameters with status FIX
        '''

        def checkStatus(para):
            '''
            Checks whether the status of the parameter is FIX 
            '''
            if para.getStatus() == 'fix':
                self.log.info("    - %-*s is fixed! Value is: %s" % (15, para.getName(), str(para.getValue())))

        self.log.info('')
        self.log.info("VAMPzero FIX: for component: %s" % self.id)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                checkStatus(para)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.inputer()

    # Sensitivity
    def sensitivity(self):
        '''
        Creates a Sensitivity representation
        '''

        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero Sensitivity")
        self.log.info("sensitivity for all parameters will be calculated")
        self.log.info("##############################################################################")

        # create file for sensitivity data
        with open('ReturnDirectory/sensitivities.csv', 'w') as senseFile:
            self.sense(self, senseFile)

        self.log.info("VAMPzero SENSE: done.")

    def sense(self, myAircraft, senseFile=None):
        '''
        **Do not use**

        This is the recursive child of sensitivity

        Recursive method for finding all parameters and calculating sensitivities

        .. todo:

           after a sensitivity run the calculation of payloadRange Diagramm fails.
           Should check whether parameters are fixed to early!
        '''

        self.log.info('')
        self.log.info("VAMPzero SENSE: for component: %s" % self.id)

        # @note: this might hurt a little
        reload(matplotlib)
        # @todo: find a solution to get the hidden matplotlib folder or pray for a solution in tcl/tk
        if os.path.isfile('C:\\Dokumente und Einstellungen\\boeh_da\\.matplotlib\\fontList.cache'):
            os.remove('C:\\Dokumente und Einstellungen\\boeh_da\\.matplotlib\\fontList.cache')

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                para.complexify()
                para.sense(myAircraft, senseFile)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.sense(myAircraft, senseFile)

    # AutoCalc
    def preCalc(self, debug, i):
        self.log.info('VAMPzero CALC: Iteration %s' % str(i))
        self.calc(discipline='')
        if debug:
            self.report()

    def calcAuto(self, discipline='', deviationAmplitude=0.0, debug=False):
        '''
        Call Calc for self
        Validate Self
        if validation gives back an error than rerun
        Quit if Calc is called more than 2000 times

        ...todo :

           Capsle the initialising loops into a single routine
        '''

        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero CALCAuto")
        self.log.info("calculation run will be repeated till converged")
        self.log.info("##############################################################################")

        count = 6

        # Do some preruns to make it nicer
        for i in range(count):
            self.preCalc(debug, i)

        while not self.converge(True):
            self.log.info('VAMPzero CALC: Iteration %i', count)
            
            try:
                self.calc(discipline, deviationAmplitude)
            except OverflowError:
                self.log.info("##############################################################################")
                self.log.info("##############################################################################")
                self.log.error("VAMPzero CALC: An Overflow Error in Python occurred.")
                self.log.error("VAMPzero CALC: Probably Your Calculation is not Converging")
                self.log.error("VAMPzero CALC: Closing without success")
                printFooter()
                exit()#@note: enter exit code here

            if debug:
                self.report()
            count += 1
            if count > 2000:
                self.log.info("##############################################################################")
                self.log.info("##############################################################################")
                self.log.error("VAMPzero CALC: more than " + str(count) + " Iterations in calcAuto, hence quitting")
                printFooter()
                raise NotConvergingError()
#                exit()#@note: enter exit code here

        self.log.info("VAMPzero CALCAuto: done.")

    def calc(self, discipline='', deviationAmplitude=0.0):
        '''
        Will Call the calc'discipline' method for all objects (including self) that own this method
        if discipline = '' all disciplines will be called that are part of the discipline List 
        '''
        disciplineList = ['Atmosphere', 'Geometry', 'Mass', 'CoG', 'Inertia', 'Mission', 'Aerodynamic', 'Cabin',
                          'Propulsion', 'Sizing', 'CPACS']

        # Call your own routines
        if discipline == '':
            discipline = disciplineList

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)
            # If it is a parameter
            if issubclass(para.__class__, parameter):
                try:
                    para.calc()
                    if deviationAmplitude != 0.0 and para.hasDeviation():
                        devFactor = deviationAmplitude * para.getDeviationFactor()
                        delta = devFactor*para.getDeviation()*para.getValue()
                        '''
                        The following line sets the parameters value without adding the new value to the history.
                        This avoids an oscillation of the parameter in the history.
                        '''
                        if not cmp(para.getStatus(), 'fix') == 0:
                            para.setValue(para.getValue() + delta)
                except ValueError:
                    self.log.debug("VAMPzero MATH: Error in the calculation of: %s" % para.longName)
                except ZeroDivisionError:
                    self.log.debug("VAMPzero MATH: Zero Division Error in the calculation of: %s" % para.longName)
                except RuntimeWarning:
                    self.log.debug("VAMPzero MATH: Zero Division Error in the calculation of: %s" % para.longName)
                except TypeError:
                    self.log.debug("VAMPzero MATH: Type Error in the calculation of: %s" % para.longName)
                except OverflowError, e:
                    print e, para['name'], para['value']
                    self.log.debug("########### %s, %s, %s" %(e, para['name'], para['value']))

        # Call everyone that is under yourself!
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)
            # Case 1 discipline is defined by user
            if hasattr(para, 'level') and issubclass(para.__class__, component):
                # Only call topdown
                if para.level > self.level:
                    para.calc(discipline, deviationAmplitude)

    # Export to CPACS
    def cpacsExport(self, CPACSObj):
        '''
        This methods exports all parameters nested in the component.
        Nested Components will be called as well.
        cpacsExport takes a CPACSObj that is an object from the CPACS class
        derived from the XML Schema Definition of CPACS
        '''
        self.exporter(CPACSObj)

    def exporter(self, CPACSObj):
        '''
        **Do not use only for system use**

        This is the recursive child of cpacsExport
        '''
        # go through all Parameters of self
        # distinguish between the two types parameter and component
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)
            # if paramter and cpacsPath valid build up tree and add value
            if issubclass(para.__class__, parameter):
                # this is a small workaround to make sure that there are no complex numbers left before exporting
                if issubclass(type(para.getValue()), complex):
                    para.setValue(para.getValue().real)
                    para.realify()

                para.cpacsExport(CPACSObj)

        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)
            # if para is a subclass of component call the exporter again
            # check as well if para is of a lower level so that it will be called top down
            if issubclass(para.__class__, component) and para.level > self.level:
                para.cpacsExport(CPACSObj)

    # Export to Freemind
    def freemindExport(self, folder='.\\ReturnDirectory\\', withValues=True):
        '''
        This methods exports all parameters nested in the component.
        Nested Components will be called as well.
        Folder is an optional argument that specifies the output location of the mindMaps
        withValues specifies whether the values are included in the output or not.
        '''
        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero Freemind Export to %s" % folder)
        self.log.info("creating Mindmaps for all parameters")
        self.log.info("##############################################################################")
        self.freemind(folder, withValues=withValues)
        self.log.info("VAMPzero MIND: done.")


    def freemind(self, path, withValues=True):
        '''
        **Do not use only for system use**

        This is the recursive child of freemindExport
        '''
        self.log.debug("VAMPzero MIND: for component: %s" % self.id)

        # go through all Parameters of self
        # distinguish between the two types parameter and component
        for para in sorted(self.__dict__, key=str.lower):
            para = getattr(self, para)

            # if paramter and cpacsPath valid build up tree and add value
            if issubclass(para.__class__, parameter):
                para.freemindExport(withValues=withValues)

               #if para is a subclass of component call the exporter again
               #check as well if para is of a lower level so that it will be called top down
            if issubclass(para.__class__, component) and para.level > self.level:
                para.freemind(path, withValues=withValues)

    # Import from CPACS
    def cpacsImport(self, path='.\\cpacs.xml'):
        '''
        Looks for parameter.CPACSPath in CPACSFilse defined by Path
        Transfers Value is possible
        Input Values will be set to 'fix' 
        '''
        self.log.info('')
        self.log.info("##############################################################################")
        self.log.info("VAMPzero CPACS Import from %s" % path)
        self.log.info("trying to import and fix parameters")
        self.log.info("##############################################################################")

        TIXIHandle = openTIXI(path)
        modelUID = getText(TIXIHandle, '/cpacs/toolspecific/vampZero/aircraftModelUID')

        if modelUID is None:
            self.log.info("VAMPzero IMPORT: No modelUID specified in the toolspecific Block")
            try:
                modelUID = self.modelUID.getValue()
                self.log.info("VAMPzero IMPORT: loaded modelUID from VAMPzero")
            except AttributeError:
                modelUID = None
                self.log.info("VAMPzero IMPORT: could not load modelUID from VAMPzero")

        if modelUID is not None:
            TIGLHandle = openTIGL(TIXIHandle, modelUID)
            if TIGLHandle is not None:
                self.log.debug("VAMPzero IMPORT: Opened TIXI and TIGL in Component")
        else:
            TIGLHandle = None
            self.log.debug("VAMPzero IMPORT: Opened only TIXI in Component as no modelUID was specified")

        self.importer(path, TIXIHandle, TIGLHandle)
        self.log.info("VAMPzero IMPORT: done.")

        closeXML(TIXIHandle)

    def importer(self, path, TIXIHandle, TIGLHandle):
        '''
        do not use for System use only!!!
        Calls the Parameter.cpacsImport or itsself recursively
        '''
        # go through all Parameters of self
        # distinguish between the two types parameter and component
        for para in self.__dict__:
            para = getattr(self, para)

            # if paramter and cpacsPath valid build up tree and add value
            if issubclass(para.__class__, parameter):
                try:
                    #self.log.debug("STATUS: %s, \t\t%s" %(para['name'], para.getStatus()))
                    if para.getStatus() == 'calc':
                        # if the parameter is set to calc in the toolspecific part,
                        # then keep it calc even after the import
                        # this might be usefull when some geometry parameters are allowed to change
                        para.cpacsImport(path, TIXIHandle, TIGLHandle)
                        para["status"] = 'calc'
                    elif para.getStatus() != 'fix':
                        para.cpacsImport(path, TIXIHandle, TIGLHandle)
                    else:
                        # check whether a parameter would have been importet from CPACS otherwise
                        # if so, throw a warning
                        if para.getCpacsPath() != '' or ('Parameter' not in str(inspect.getmodule(para.cpacsImport))):
                            self.log.warning("CPACS Import prevented. Given in toolspecific: %s" % para.longName)
                except TypeError:
                    para.cpacsImport(path)
                    self.log.debug("VAMPzero Import TypeError for Parameter: %s" % para.longName)

            # if para is a subclass of component call the importer again
            # check as well if para is of a lower level so that it will be called top down
            if issubclass(para.__class__, component) and para.level > self.level:
                try:
                    para.importer(path, TIXIHandle, TIGLHandle)
                except TypeError:
                    self.log.debug("VAMPzero Import TypeError for Component: %s" % para.id)

    # Import from GUI
    def guiImport(self, path='.\\cpacs.xml'):
        '''
        Looks for parameter in CPACSFile defined by component.discipline.name
        Input Values will be set to 'fix'
        '''
        importGUI(self, path)

    # Plotting
    def plotter(self, ax):
        '''
        Recursive call for the validation of Convergence in VAMPzero
        This method goes through all parameters and collects their history
        The data is then displayed in the ConvergencePlot
        '''

        # Go through all user declared attributes
        for para in self.__dict__:
            para = getattr(self, para)

            #If para is parameter do the validation
            if issubclass(para.__class__, parameter):
                if type(para["history"][0]) == int or type(para["history"][0]) == float and para["status"] == 'calc' and para["history"][-1] != 0.:
                    x = [x / para["history"][-1] for x in para["history"] if x != 0.]
                    y = range(len(x))
                    ax.plot(y, x, label=para["name"])

        for para in self.__dict__:
            para = getattr(self, para)

            #If para is component call yourself
            if issubclass(para.__class__, component) and para.level > self.level:
                para.plotter(ax)

    def plot(self):
        '''
        Calls the plotAircraft function from lib.matplotlib
        '''
        plotAircraft(self)
