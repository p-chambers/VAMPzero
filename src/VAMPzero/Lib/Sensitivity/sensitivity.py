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
from __future__ import division
from VAMPzero.Lib.Matplotlib.Plots.plotSensitivityBar import plotSensitivityBar, \
    plotSensitivityBarDoc
from VAMPzero.Handler.Types import zeroComplex


def resetParameter(origStatus, parameter):
    '''
    Restores the parameters status as well as the
    status of each callee
    '''
    parameter.setStatus(origStatus)

    #for item in parameter["callee"]:
    #    item.realify()

    parameter.calc()
    #parameter.realify()


def calcSensitivities(parameter, myAircraft):
    '''
    function to calculate the sensitivity for a parameter in dependency to its callers
    will change the value for the callee +-1% and recalculate the parameter
    @param parameter: The Parameter that is the parent for the to calculate callee sensitivities
    @param myAircraft: best a converged aircraft   
    '''

    #Some Lists
    ups = []
    lows = []
    names = []
    count = 1

    #parameter value for comparison
    orig = parameter.getValue()
    origStatus = parameter.getStatus()
    parameter.setStatus('calc')

    #Check whether we can compare
    if type(orig) == zeroComplex:

        #now go through all callees
        for item in parameter["callee"]:
            #and check whether we can change them in a way that makes sense
            item.complexify()
            if type(item.getValue()) == zeroComplex:
                #old callee values 
                old = item.getValue().real
                delta = 0.000000001j

                #split name
                if item.longName.find('aircraft') == -1:
                    name = item.longName
                else:
                    name = item.longName.split('.')[1]

                if not item.longName.find('airfoil') == -1:
                    break

                #save the found name
                names.append(name)

                #find upper value
                item.setValue(old + delta)
                parameter.calc()

                try:
                    up = parameter.getValue().imag
                except:
                    up = 0.
                ups.append(up / delta.imag * old)

                #find lower value
                item.setValue(old - delta)
                parameter.calc()

                try:
                    low = parameter.getValue().imag
                except:
                    low = 0.
                lows.append(low / delta.imag * old)

                #reset
                count += 1
                item.setValue(old)
                parameter.calc()
                parameter.log.debug(
                    "VAMPzero SENSE: Sensitivity %s from %s: up: %s and low: %s " % (str(parameter.longName), str(item.longName), str(up), str(low)))

    resetParameter(origStatus, parameter)
    return names, ups, lows


def createSenseBar(parameter, names, ups, lows, doc=False, calcName=''):
    '''
    function to create the sensitivity bars for a parameter.
    '''

    if not doc:
        plotSensitivityBar(parameter.longName, names, ups)
    else:
        plotSensitivityBarDoc(parameter, names, ups, calcName)


def writeSenseToFile(senseFile, parameter, names, ups, lows):
    '''
    function to write the sensitivities to a file
    @param senseFile: file handle
    '''
    # write sensitivities to a file
    assert (len(names) == len(ups) and len(names) == len(lows))
    zipped = [(x[0], str(x[1]), str(x[2])) for x in zip(names, ups, lows)]
    line = parameter.longName + ';' + str(len(names)) + ';' + ';'.join([';'.join(par) for par in zipped])
    senseFile.write(line + '\n')

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################    
