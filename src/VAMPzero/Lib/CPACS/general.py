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
from math import pi, sqrt
import inspect
import sys
import time
from numpy.lib.function_base import interp

from VAMPzero.Lib.Log.log import zeroLogger


global t0




rad = pi / 180.

log = zeroLogger('General')

def printHeader():

    #choosing the appropriate splitter for the running filename
    if sys.platform == 'win32':
        splitter = '\\'
    else:
        splitter = '/'

    
    log.info("##############################################################################")
    log.info("                                    VAMPzero                    ") 
    log.info("                      Conceptual design as it should be      ")
    log.info("                                              ")
    log.info("                 Licensed under the Apache License, Version 2.0 ")
    log.info("                   http://www.apache.org/licenses/LICENSE-2.0          ")
    log.info("           (c) 2012 Deutsches Zentrum fuer Luft- und Raumfahrt e.V.")
    log.info("                                              ")    
    log.info("                  code written by Daniel Boehnke at DLR-LY-IL ")   
    log.info("                  further sources are highlighted within code ")
    log.info("                        contact at daniel.boehnke@dlr.de        ")   
    log.info("                              +49 40 42878 4447               ")
    log.info("                        Blohmstrasse 18, 21079 Hamburg          ")
    log.info("##############################################################################")
    log.info("                                    Running                                     ")
    log.info("                             %s"%inspect.stack()[-1][1].split(splitter)[-1])
    log.info("      On %s"%sys.version)
    log.info("##############################################################################")
    log.info("##############################################################################")

    #linking stderr to log!!
    #sys.stderr = log
    log.debug('linked stderr to logstream')
    
    global t0
    t0= time.clock()
    log.debug('starting time is %s'%str(t0))

def printFooter():

    log.info("")
    log.info("##############################################################################")
    log.info("                                    VAMPzero                    ")
    log.info("                                    FINISHED                    ")

    try:
        global t0
        t1 = time.clock()-t0
        log.info("                            %-4.2f seconds passed                      "% t1)
    except NameError:
        pass

    log.info("##############################################################################")
    log.info("##############################################################################")
    

def mittelwert(werte):
    n=len(werte)
    summe = 0
    for i in werte: 
        summe=summe+i 
    
    if n:
        return summe/n
    else:
        return summe

def pointDistance(x1,y1,z1,x2,y2,z2):
    '''
    Calculates the distance between two points defined by their cartesian coordintes x1,y1,z1 and x2,y2,z2 
    '''
    return sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

def evalList(List):
    '''
    Method to eval all values in a List
    
    returns List
    '''
    newList = []
    
    for item in List:
        if item != '' and item != None:
            newList.append(eval(item))
            
    return newList

def interpolateList(x1,x2,xn,y1,y2):
    '''
    Function to interpolate between lists y1 and y2 that are located at 
    x1 and x2. Returns a new list yn at xn. Interpolation is done linear
    '''
    yn = []
    for i in range(len(y1)):
        j = interp(xn,[x1,x2],[y1[i],y2[i]])
        yn.append(j)
    
    return yn

def findHigher(x,y):
    '''
    finds the next higher neighbor to x in y
    '''
    ySort = sorted(y)
    
    #Go through all values of the sorted list. The first result of x-i that is negative
    #gives the value that is higher than x
    for i in ySort:
        if x-i<0. : 
            return i
        
def findLower(x,y):
    '''
    finds the next lower neighbor to x in y
    '''
    ySort = sorted(y, reverse= True)

    #Go through all values of the reverse sorted list. The first result of x-i that is positive
    #gives the value that is lower than x

    for i in ySort:
        if x-i>0. : 
            return i

def chunks(l, n):
    ''' 
    Yield successive n-sized chunks from l. Works. Don't ask me how!
    
    :Source: stackoverflow
    :Author: Ned Bachelder
    '''
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
    

