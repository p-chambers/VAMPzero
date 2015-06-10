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

from numpy.lib.function_base import interp

def getCDcri(CLcr,CfxList,CfzList,AOAList):
    '''
    Interpolation function to get the CD value for cruise induced drag 
    '''
    AOAcr       = interp(CLcr,CfzList,AOAList)
    CDcri       = interp(AOAcr,AOAList, CfxList)
    return CDcri 

        
def getAeroData(CfxList,CfzList,refArea,wingAref):
    '''
    Gives the Aeroperformance Values as Vectors 
    Adjust Lifting Line input, as Cf values are related to the Reference Area in the CPACS File
    , whereas they are related to the WingApprox Area
    '''
    for i in range(len(CfxList)):
        CfxList[i-1] = CfxList[i-1] * refArea / wingAref

    for i in range(len(CfzList)):
        CfzList[i-1] = CfzList[i-1] * refArea / wingAref

    return CfxList,CfzList