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
from VAMPzero.Lib.Log.log import zeroLogger


        
        
def importMatlab(myAircraft,path="./ToolInput/toolInput.m"):
    '''
    This is an import routine for simple input from an m-File. m Files can be created using Matlab. 
    This import routine enables users to loop VAMPzero easily by placing input statements
    into the file specified by the path parameter.

    It takes an *aircraft* as input. This is necessary to set the values in
    the aircraft according to the information given in *path*. Usually
    *path* is specified as ./ToolInput/toolInput.m
    
    The structure of the m-File should be a simple as possible. It will be just a plain list of values. The value
    names are a combination of component and parameter. For each parameter their may be an additional factor:
    
    *aircraft.mTOM=73500;
    *engine.sfcCR.factor=0.97; 
    
    This would result in a new maximum takeofff weight of 73.5t and a calibration factor for the SFC of the engine in 
    cruise condition of 0.97
    '''
    log = zeroLogger('General')
    log.info('')
    log.info("##############################################################################")
    log.info('VAMPzero MATLAB: importing values from: %s'%path)
    log.info("reading matlab inputs")
    log.info("##############################################################################")
    

    myFile  = open(path,'r')
    myLines = myFile.readlines() 
    
    for line in myLines:
        valueP  = ''
        factorP = ''        
        backup  = line
        nameC   = line.split('.')[0]
        nameP   = line.split('.')[1].split('=')[0]
        if line.find('factor')!=-1:
            factorP = backup.split('=')[1].replace(';','')
        else:
            valueP  = backup.split('=')[1].replace(';','')
            
        setParameter(myAircraft, nameC, nameP, valueP,factorP)
        

def setParameter(myAircraft,nameC,nameP,valueP,factorP):
    '''
    will try to set a value from importGUI input
    '''
    nameC = nameC.capitalize()
    if not cmp(nameC, 'Htpairfoil'):
        nameC='htp.htpairfoil'

    if not cmp(nameC, 'Vtpairfoil'):
        nameC='vtp.vtpairfoil'

    if not cmp(nameC, 'Wingairfoil'):
        nameC='wing.wingairfoil'
    
    if not cmp(nameC, 'Aircraft'):
        nameC=''

    if not cmp(nameC, 'Landinggear'):
        nameC='landingGear.'
    
    if not cmp(nameC,'')==0 and not cmp(nameC,'landingGear.')==0:
        nameC = nameC.lower()+'.'
    
    log = zeroLogger('General')
    
    if factorP != '' and not factorP is None:
        try:
            command = str('myAircraft.'+nameC+nameP+'.setFactor('+factorP+')')
            log.debug('VAMPzero MATLAB: executing %s'%command)
            exec command
        except:
            log.warning('VAMPzero MATLAB: no success in: %s'%command)

    if valueP != '' and not valueP is None:
        try:
            command = str('myAircraft.'+nameC+nameP+'.setValueFix('+valueP+')')
            log.debug('VAMPzero MATLAB: executing %s'%command)
            exec command
        except:
            log.warning('VAMPzero MATLAB: no success in: %s'%command)


