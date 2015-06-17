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

from numpy import array, complex128
import inspect
import sys
import random

import VAMPzero
from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath
from VAMPzero.Lib.Freemind.freemind import zeroNode
from VAMPzero.Lib.Log.log import zeroLogger
from VAMPzero.Lib.Sensitivity.sensitivity import createSenseBar, writeSenseToFile, calcSensitivities
from VAMPzero.Lib.TIXI.tixi import openTIXI, getText
from VAMPzero.Lib.Sphinx.createParameterDoc import createParameterDoc
from VAMPzero.Handler.Types import zeroComplex


# added this function to retrieve the discipline from parent folder
if sys.platform == 'win32':
    splitter = '\\'
else:
    splitter = '/'

class parameter(dict):
    '''
    **Superclass for all Parameters**
    
    A parameter holds the design knowledge in VAMPzero. All parameters in the model need to inherit this class.
    
    Each parameter holds several attributes: 
    
    * value
      
      The value of the parameter in the corresponding unit. 
      
    * factor
    
      Each parameter can hold a factor. These technology 
      factors can be used to 
      calibrate the calculation or introduce technologies 
      not directly modelled in VAMPzero.
      
    * unit
    
      The unit of the parameter. Although units can be arbitrary strings, VAMPzero tries to stick to SI-units.
      
    * status
    
      The status of a parameter influences the actions taken during the calculation. It can have different values: 
      
        * **fixed** by user input, may not be changed during the calculation 
        * *init* the parameter was not altered during the calculation
        * calc the parameter was calculated 
      
    * cpacsPath
    
      The cpacsPath is an optional attribute. If it is given value will be imported/exported to the respective location in CPACS. 
    
    For the methods of parameter see the following documentation. Please note that some of these routines maybe overwritten.  
    '''

    # Adjacence is important for the mindmaps and setting content of caller and callee keys
    doAdjacence = True

    # If this is set to True VAMPzero will call its callee if its value is set by a setValueCalc
    doCalleeCalc = False

    # If this is set to True VAMPzero will call its caller if its value is set by a setValueCalc
    doCallerCalc = False

    # If this is set to true, we switch to complex mode for the sensitivities
    isComplex = False

    # This is a small container for saving results
    resultList = []

    def __init__(self, value=0.0, unit='', status='init', doc='Default Doc', factor=1., cpacsPath='', name='',
                 parent='', **kwargs):

        def setname(me):
            '''
            Returns the name of the parameter from its type definition
            '''
            return str(type(me)).split('\'')[1].split('.')[-1]

        def setparent(me):
            '''
            finds the parent component from the caller frames
            This will only work if a parameter is constructed from a component
            not from a toplevel script
            first frame is this function
            second is the constructor of the parameter
            third is the component
            '''
            try:
                frame = inspect.currentframe().f_back.f_back.f_back.f_locals
            except:
                me.log.warning('VAMPzero CONSTRUCTOR: Could not find parent for : %s: ' % me.getName())

            try:
                caller = frame['self']
            except:
                caller = None
                me.log.warning('VAMPzero CONSTRUCTOR: Could not find parent for : %s: ' % me.getName())

            if issubclass(type(caller), VAMPzero.Handler.Component.component):
                return caller
            else:
                # try the same for one frame more if there is no parameter specific constructor
                # note: this could probably done recursively as it goes done more frames, but I would 
                # think this may end in loops to quick 
                try:
                    frame = inspect.currentframe().f_back.f_back.f_locals
                except:
                    me.log.warning('VAMPzero CONSTRUCTOR: Could not find parent for : %s: ' % me.getName())

                try:
                    caller = frame['self']
                except:
                    me.log.warning('VAMPzero CONSTRUCTOR: Could not find parent for : %s: ' % me.getName())

                if issubclass(type(caller), VAMPzero.Handler.Component.component):
                    return caller

        self.log = zeroLogger(setname(self))
        self.parent = parent

        self["value"] = value  # The parameters value
        self["unit"] = unit  # it's unit, if possible please stick to metric units
        self["status"] = status  # it's status, init,calc or fix
        self["doc"] = doc  # the documentation string
        self["factor"] = factor  # the technology factor
        self["cpacsPath"] = cpacsPath  # the cpacsPath in X-Path notation
        self["caller"] = []  # a list of parameters who's calculations called the parameter
        self["callee"] = []  # a list of parameters that have been called by this parameter
        self["history"] = []  # the calculation history
        self["history"].append(self["value"])
        self["name"] = setname(self)
        self["stdDeviation"] = None
        self["devFactor"] = random.gauss(0.0, 1.0) # (mean, std deviation)
        self["exportTS"] = False

        # get the discipline from the folder name!
        discipline = inspect.stack()[1][1].split(splitter)[-2]
        self["discipline"] = discipline

        if parent == "":
            self.parent = setparent(self)
        else:
            self.parent = parent

        self.longName = self.parent.id + '.' + self['name']
        self.count = 0

    # Help String
    def help(self):
        '''
        Returns a help String similar to Matlab
        '''
        try:
            result = "%1.3f" % self["value"]
        except:
            result = str(self["value"])
        self.log.info(
            'VAMPzero HELP: %-*s in [%-*s], value: %s' % (19, str(self["name"]), 5, str(self["unit"]), result))

    # Getter
    def getUnit(self):
        '''
        Returns the unit of the parameter
        '''
        return self["unit"]

    def getName(self):
        '''
        Returns the name of the parameter
        '''
        return self["name"]

    def getFactor(self):
        '''
        Returns the technology factor of the parameter
        '''
        return self["factor"]

    def getDiscipline(self):
        '''
        Returns the discipline of the parameter
        '''
        return self["discipline"]

    def getStatus(self):
        '''
        Returns the statur of the parameter
        '''
        return self["status"]

    def getCpacsPath(self):
        '''
        Returns the cpacs Path of the parameter
        '''
        return self["cpacsPath"]

    def getHistory(self):
        '''
        Returns the calculation history of the parameter
        '''
        return self["history"]

    def getValue(self):
        '''
        The function getValue returns the value of a parameter. 
        
        If the doAdjacence switch is set to true it tries to resolve the dependencies in the code, 
        i.e. it logs which parameter tries to execute getValue(). If a parameter triggers getValue
        this means that it relies on a parameter for the calculation. 
        
        This information is very important for a designer. E.g. If you look up a book and try to 
        find information how to calculate the wings reference area this is easy. Just look up the page.
        But if you want to find out which parameter is influenced by the wing area you have to 
        look through all pages of the book and find out if the wing area is used in a formula. 
        
        * Caller
        
          A Caller is a parameter that call's for it's own calculation of this value, 
          i.e. it is on the left hand side of the equation
          
        * Callee
        
          A Callee is called by this parameter, i.e. it is on the right hand side of the equation
        
        '''
        if parameter.doAdjacence: # using class variable
            # Get the parent caller
            frame = inspect.currentframe()

            caller = frame.f_back.f_locals
            try:
                caller = caller['self']
            except:
                pass

            if issubclass(type(caller), parameter):
                # Append Caller
                appendCaller = True
                for item in self['caller']:
                    if caller.longName == item.longName:
                        appendCaller = False

                if appendCaller or len(self['caller']) == 0:
                    self['caller'].append(caller)

                # Append Callee in Caller
                appendCallee = True
                for item in caller['callee']:
                    if item.longName == self.longName:
                        appendCallee = False

                if appendCallee or len(caller['callee']) == 0:
                    if not caller.longName == self.longName:
                        caller['callee'].append(self)

        # back to baseline getValue function
        if type(self["value"]) in (float, int, array):
            return self["value"]
        else:
            return self["value"]

    def getDeviation(self):
        return self["stdDeviation"]
    
    def getDeviationFactor(self):
        '''
        Factor which is multiplied with the standard deviation.
        Percentage of standard deviation to be applied.
        '''
        return self["devFactor"]

    # Check if standard deviation is set
    def hasDeviation(self):
        return self["stdDeviation"] != None

    # Setters
    def setUnit(self, unit=''):
        '''
        Sets the unit of the parameter
        '''
        self["unit"] = unit
        return self["unit"]

    def setName(self, name=''):
        '''
        Sets the unit of the parameter
        '''
        self["name"] = name
        return self["name"]

    def setFactor(self, factor=''):
        '''
        Sets the technology factor for a parameter. 
        
        If factor is not unity it will be applied to the value directly
        '''
        self["factor"] = factor
        if factor != 1.:
            self.setValue(self["value"] * factor)

        return self["factor"]

    def setDiscipline(self, discipline=''):
        '''
        Sets the unit of the parameter
        '''
        self["discipline"] = discipline
        return self["discipline"]

    def setStatus(self, status=''):
        '''
        Sets the status of the parameter
        '''
        self["status"] = status
        return self["status"]

    def setCpacsPath(self, cpacsPath=''):
        '''
        Sets the cpacsPath of the parameter
        '''
        self["cpacsPath"] = cpacsPath
        return self["cpacsPath"]

    def setHistory(self, history=''):
        '''
        Sets the history of the parameter
        '''
        self["history"] = history
        return self["history"]

    def setDeviation(self, stdDeviation):
        """
        Sets the standard deviation of the parameter
        """
        self["stdDeviation"] = stdDeviation
    
    def setDeviationFactor(self, value):
        '''
        Factor which is multiplied with the standard deviation.
        Percentage of standard deviation to be applied.
        '''
        self["devFactor"] = value

    def setValue(self, value=''):
        '''
        Sets the value for a parameter!
        
        The behaviour of this function is dependent on the parameter.isComplex switch
        If isComplex is true all values need to be converted to zeroComplex. 
        If isComplex is false value should only have a real part 
        '''

        # Do this if NO complex values are wanted
        if not parameter.isComplex:
            if type(value) == complex or type(value) == zeroComplex:
                self["value"] = value.real
            else:
                self["value"] = value

        # Do this if complex values are wanted
        else:
            try:
                self["value"] = zeroComplex(value)
            except ValueError:
                self.log.error(
                    "VAMPzero Complex: Could not transfer the value for %s to zeroComplex Type. Value is: %s" % (
                        self.longName, str(value)))

        return self["value"]

    def setValueFix(self, value=0.):
        '''
        This method is called to enter a value to a parameter and fix it, 
        so that it can not be changed during a calculation. A User Input is a good example
        application of this funtion: 
        
        * parameter["value"] will be set to the given value 
        * parameter["status"] will be set to 'fix'
        '''
        self["status"] = 'fix'

        try:
            self.setValue(value * self["factor"])
        except TypeError:
            self.setValue(value)
            self.log.debug("VAMPzero setValue: Could not apply factor to paramter: %s" % self.longName)

        return self["value"]

    def setValueCalc(self, value=0.):
        '''
        Each calc() function of a parameter will use this method to store its result. setValueCalc will not 
        overwrite the value of a parameter that has the status 'fix'
        
        If the status of the parameter unequals 'fix' then this method will set the status to 'calc'
        
        Furthermore, this method adds the value to the parameter's calculation history so that 
        convergence checks can be run.  
        '''
        if not cmp(self.getStatus(), 'fix') == 0:
            # Set Value
            try:
                self.setValue(value * self["factor"])
            except TypeError:
                self.setValue(value)
                self.log.debug("VAMPzero setValue: Could not apply factor to paramter: %s" % self.longName)

            # Set Status
            self.setStatus('calc')

            # Set History
            if type(value) == float or type(value) == int:
                self.getHistory().append(value)
            elif type(value) == zeroComplex or type(value) == complex or type(value) == complex128:
                self.getHistory().append(value.real)
            else:
                pass

        return self["value"]

    # Complex methods
    def complexify(self):
        '''
        Tries to convert the own value to a zeroComplex value
        is necessary for the complex-step calculation of the sensitivities
        '''
        try:
            self["value"] = zeroComplex(self["value"])
            parameter.isComplex = True
        except ValueError:
            self.log.debug("VAMPzero COMPLEX: could not convert %s to zeroComplex, value is: %s" % (
                self.longName, str(self["value"])))
            return False

    def realify(self):
        '''
        Tries to convert the own value to a real value
        is necessary for the complex-step calculation of the sensitivities
        '''
        if type(self["value"]) != str:
            try:
                self["value"] = self["value"].real
                parameter.isComplex = False
            except ValueError, AttributeError:
                self.log.debug(
                    "VAMPzero REAL: could not convert %s to real, value is: %s" % (self.longName, str(self["value"])))

    # Check for Convergence
    def checkConvergence(self):
        '''
        Checks whether the parameter seems to have converged
        it will be checked whether the value has changed more than 10-5% from the last calculation 
        '''

        # Don't even get started if you are fixed
        if self.getStatus() == "fix" or self.getStatus() == "init":
            return True

        # Get the actual value
        if type(self.getHistory()[-1]) == zeroComplex:
            this = self.getHistory()[-1].real
        elif type(self.getHistory()[-1]) == float:
            this = self.getHistory()[-1]
        elif type(self.getHistory()[-1]) == int or type(self.getHistory()[-1]) == str:
            return True
        else:
            this = 0.

        # Do the Check
        if this != 0. and len(self.getHistory()) > 2:
            # Get the second value
            if type(self.getHistory()[-2]) == zeroComplex:
                last = self.getHistory()[-2].real
            # if the starting value is an integer it still might change to a float during iteration
            # therefore the second last value could also be an integer
            elif type(self.getHistory()[-2]) == float:
                last = self.getHistory()[-2]
            else:
                self.log.warning("unexpected type of history value: %s" % (type(self.getHistory()[-2])))
                last = self.getHistory()[-2]
                # Check equals the ratio of the last two history values -1
            check = last / this - 1.

            if abs(check) < 0.00001:
                # append value to history to mark convergence
                self.getHistory().append(self.getHistory()[-1])
                return True

            else:
                self.log.debug("    - %-*s relative change: %-*s" % (15, self.getName(), 5, str(check)))
                return False
        else:
            return True

    def calc(self):
        '''
        Each parameter will overwrite this method with it's own calculation methods
        
        Strictly, speaking the method could also throw a warning if called
        '''
        pass

    def freemindExport(self, depth=3, withValues=True):
        '''
        Creates a Mindmap from caller and callee entries and exports it
        '''
        myNode = zeroNode(self, withValues=withValues, initial=True)

        if not cmp(self.getStatus(), 'fix') == 0:
            myNode.appendNodes(self, depth, withValues=withValues)

        myNode.appendLeftNodes(self, withValues=withValues)
        myNode.createMindMap()

    def sense(self, myAircraft, senseFile=None, doc=False, name=''):
        '''
        Create a sensitivity plot
        @param senseFile: file handle
        '''
        parameter.isComplex = True
        self.complexify()
        try:
            names, ups, lows = calcSensitivities(self, myAircraft)
            createSenseBar(self, names, ups, lows, doc, name)
            if senseFile!=None:
                writeSenseToFile(senseFile, self, names, ups, lows)
        except TypeError, e:
            self.log.warning(
                "VAMPzero SENSE: Sensitivity of %s could not be calculated due to the following error: %s" % (
                    self.longName, str(e)))

    def cpacsExport(self, CPACSObj):
        '''
        this methods exports self.value to self.cpacsPath in path 
        cpacsPath must be filled
        path is an optional argument for the output
        Additionally, all values are parsed into the resultList so that they can be exported later on
        '''
        if self.getCpacsPath() != '':
            para = getObjfromXpath(CPACSObj, self.getCpacsPath())
            # the value has to be string for the cpacslib to work
            para.set_valueOf_(str(self.getValue()))
            self.log.debug(
                "VAMPzero EXPORT: %s = %s exported to %s" % (self.longName, para.get_valueOf_(), self.getCpacsPath()))

        if type(self.getValue()) == str:
            parameter.resultList.append(str(self.longName + '=\'' + str(self.getValue()) + '\';\n'))
        else:
            parameter.resultList.append(str(self.longName + '=' + str(self.getValue()) + ';\n'))

    def resultExport(self, fileHandle):
        '''
        writes all entries from the resultList into VAMPzero.m file
        '''
        value = None
        # check whether the parameter is complex
        if issubclass(type(self.getValue()), complex):
            value = self.getValue().real
        else:
            value = self.getValue()
        
        resultLine = None
        if type(self.getValue()) == str:
            resultLine = str(self.longName + '=\'' + str(value) + '\';\n')
        else:
            resultLine = str(self.longName + '=' + str(value) + ';\n')
        fileHandle.write(resultLine)

    def cpacsImport(self, path='.\\cpacs.xml', TIXIHandle=None, TIGLHandle=None):
        '''
        TIXI and TIGL Handle should be given, to save some valueable time
        Imports self.cpacsPath from path
        Input Values will be set to 'fix' 
        '''
        if not TIXIHandle:
            TIXIHandle = openTIXI(path)

        if self.getCpacsPath() != '':
            retVal = getText(TIXIHandle, self.getCpacsPath())
            if retVal is not None and retVal is not '':
                try:
                    self.setValueFix(eval(retVal))
                    self.importSuccess()
                # This may occur if UID or other strings will be imported
                except NameError:
                    self.setValueFix(retVal)
                    self.importSuccess()
                except SyntaxError:
                    self.setValueFix(retVal)
                    self.importSuccess()

            else:
                self.importError()

    def createDoc(self, myAircraft, parentFolder):
        '''
        Creates a structured Text File so that the documentation can be created
        '''
        createParameterDoc(self, myAircraft, parentFolder)

    def importError(self):
        '''
        gets Triggered if an Import Fails
        '''
        if self.getCpacsPath() != '':
            self.log.debug('VAMPzero TIXI: %-*s could not be fetched from path:%s' % (
                19, self.parent.id + '.' + self.getName(), self.getCpacsPath()))

    def importSuccess(self):
        '''
        gets Triggered if an Import succeeds
        '''
        if self.getCpacsPath() == '':
            cpacs = 'own import routine'
        else:
            cpacs = self.getCpacsPath()

        self.log.debug('VAMPzero TIXI: %-*s read. Value equals: %-*s %s Import from: %s' % (
            19, self.parent.id + '.' + self.getName(), 10, self.getValue(), self.getUnit(), cpacs))

    def monkeyPatch(self, routine='new one'):
        '''
        prints a warning after a monkey patch
        '''
        self.log.debug('VAMPzero CALC: %-*s monkey-patched. Calc routine replaced by %s' % (
            19, self.parent.id + '.' + self.getName(), routine))
