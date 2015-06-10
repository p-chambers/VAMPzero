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
from VAMPzero.Lib.Log.log import zeroLogger

log     = zeroLogger('General')

def getNearest(FLList, FL, MA, T):
    '''
    more or **less** genius way of interpolation in TW Dat array
    '''
    def getUpLow(List, Target):
        Plus    = [99999999.,0]
        Minus   = [0.,0]


        for item in List:
            #Set the lower value for the interpolation of Flight Level
            if item[0]-Target > Minus[0]-Target and item[0]-Target < 0.:
                Minus = item
        
            #Set the upper value for the interpolation of Flight Level
            if item[0]-Target < Plus[0]-Target and item[0]-Target > 0.:
                Plus = item
        
        if List[-1][0]<Target:
            Minus = List[-2]
            Plus  = List[-1]
            log.warning('VAMPzero TWDAT: Interpolation Error need to extrapolate! Target value is: %s'% Target)
            log.warning('VAMPzero TWDAT: New up: %s and low: %s' %(Plus[0],Minus[0]))
        
        return Plus, Minus

    FLplus, FLminus                         = getUpLow(FLList,FL)
       
    FLplusMAplus, FLplusMAminus             = getUpLow(FLplus[1],MA)
    FLminusMAplus,FLminusMAminus            = getUpLow(FLminus[1],MA)
    
    FLplusMAplusTplus,FLplusMAplusTminus    = getUpLow(FLplusMAplus[1],T)
    FLplusMAminusTplus,FLplusMAminusTminus  = getUpLow(FLplusMAminus[1],T)
    FLminusMAplusTplus,FLminusMAplusTminus  = getUpLow(FLminusMAplus[1],T)
    FLminusMAminusTplus,FLminusMAminusTminus= getUpLow(FLminusMAminus[1],T)
                    
    #Do the interpolations
    SFCFLplusMaplus     = interp(T,[FLplusMAplusTminus[0],FLplusMAplusTplus[0]],[FLplusMAplusTminus[1],FLplusMAplusTplus[1]])
    SFCFLplusMaminus    = interp(T,[FLplusMAminusTminus[0],FLplusMAminusTplus[0]],[FLplusMAminusTminus[1],FLplusMAminusTplus[1]])
    SFCFLminusMaplus    = interp(T,[FLminusMAplusTminus[0],FLminusMAplusTplus[0]],[FLminusMAplusTminus[1],FLminusMAplusTplus[1]])
    SFCFLminusMaminus   = interp(T,[FLminusMAminusTminus[0],FLminusMAminusTplus[0]],[FLminusMAminusTminus[1],FLminusMAminusTplus[1]])
    

    SFCFLplus           = interp(MA,[FLplusMAminus[0],FLplusMAplus[0]],[SFCFLplusMaminus,SFCFLplusMaplus])
    SFCFLminus          = interp(MA,[FLminusMAminus[0],FLminusMAplus[0]],[SFCFLminusMaminus,SFCFLminusMaplus])

    #finally we made it!!!
    SFC                 = interp(FL,[FLminus[0],FLplus[0]],[SFCFLminus,SFCFLplus])
    return SFC
    
