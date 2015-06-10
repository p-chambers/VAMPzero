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

from VAMPzero.Lib.Freemind.freemindSchema import node, font,map, edge
from VAMPzero.Lib.Colors.colors import zeroColor, toHEX


#Get the Colors from central location! Corporate Design ftw!
aircraftC       = zeroColor["aircraft"]
wingC           = zeroColor["wing"]
fuselageC       = zeroColor["fuselage"]
engineC         = zeroColor["engine"]
atmosphereC     = zeroColor["atmosphere"]
vtpC            = zeroColor["vtp"]
htpC            = zeroColor["htp"] 
fuelC           = zeroColor["fuel"] 
systemsC        = zeroColor["systems"]
airfoilC        = zeroColor["airfoil"]
pylonC          = zeroColor["pylon"]
landingGearC    = zeroColor["landingGear"]
payloadC        = zeroColor["payload"]


class zeroFont(font):
    '''
    zeroFont class extending font from freemindSchema.py
    '''

    def __init__(self,parameter):
        super(zeroFont,self).__init__()

        self.NAME   =   "SansSerif"
        self.SIZE   =   18 

        if not cmp(parameter.getStatus(), 'fix'):
            self.set_BOLD('true')
            #self.NAME ='Serif'
        if not cmp(parameter.getStatus(), 'init'):
            self.set_ITALIC('true')
        


class zeroEdge(edge):
    '''
    zeroEdge class extending edge from freemindSchema.py
    '''
    def __init__(self,color):
        super(zeroEdge,self).__init__()
        
        self.COLOR = color
        self.STYLE = "linear"
        

        
class zeroNode(node):
    '''
    This is a zeroNode Class. It will be used to represent the parameters Information as a Nodes
    '''
    
    def __init__(self,parameter,position = 'right',withValues = True,initial = False):
        super(zeroNode,self).__init__()
        
        self.COLOR      = self.chooseColor(parameter.longName)
        self.TEXT       = self.makeName(parameter,withValues)
        self.POSITION   = position
        self.STYLE      = 'bubble'
        
        if initial: 
            self.LINK       = str('./barPlots/'+parameter.longName) + '.png'
        else: 
            self.LINK       = str(parameter.longName) + '.mm'

        self.font.append(zeroFont(parameter))
        self.edge.append(zeroEdge(self.chooseColor(parameter.longName)))
        

    def appendNodes(self,parameter,recursiveCount = 1,withValues = True):
        '''
        creates a Node Super with supnodes Sub on right side 
        '''
        if recursiveCount >0 and not cmp(parameter.getStatus(), 'fix')==0:
            for item in parameter['callee']:
                myZeroNode = zeroNode(item,withValues=withValues)
                self.add_node(myZeroNode)
                myZeroNode.appendNodes(item, recursiveCount = recursiveCount-1, withValues=withValues)
            
    def appendLeftNodes(self, parameter,withValues = True):
        '''
        creates a Node Super with supnodes Sub on right side 
        '''
        for item in parameter['caller']:
            myZeroNode = zeroNode(item,position='left',withValues=withValues)
            self.add_node(myZeroNode)


    def createMindMap(self):
        '''
        creates a new MindMap file node.TEXT.mm
        takes a node as input
        '''
        if not os.path.exists('./ReturnDirectory/mindMaps/'):
            os.makedirs('./ReturnDirectory/mindMaps/')
        
        myMap = map(version='1.0.1')
        
        myMap.set_node(self)
        myFile = open('./ReturnDirectory/mindMaps/' + self.TEXT.split()[0] + '.mm', 'w')
        myMap.export(outfile=myFile, level=0)
        myFile.close()

    def chooseColor(self,name):
        '''
        find a descent color from a containing string
        '''
        if name.find("payload") != -1:
            return toHEX(payloadC)
        if name.find("aircraft") != -1:
            return toHEX(aircraftC)
        if name.find("wing") != -1:
            return toHEX(wingC)
        if name.find("fuselage") != -1:
            return toHEX(fuselageC)
        if name.find("engine") != -1:
            return toHEX(engineC)
        if name.find("atmosphere") != -1:
            return toHEX(atmosphereC)
        if name.find("vtp") != -1:
            return toHEX(vtpC)
        if name.find("htp") != -1:
            return toHEX(htpC)
        if name.find("fuel") != -1:
            return toHEX(fuelC)
        if name.find("systems") != -1:
            return toHEX(systemsC)
        if name.find("airfoil") != -1:
            return toHEX(airfoilC)
        if name.find("pylon") != -1:
            return toHEX(pylonC)
        if name.find("landingGear") != -1:
            return toHEX(landingGearC)
        
    def makeName(self,parameter, withValue = True):
        '''
        create the name string for a zeroNode from a parameter
        if withValues is false no values will be appended
        '''
        if not withValue:
            return parameter.longName

        parameter.realify()
    
        try:
            result = "%1.3f" %parameter.getValue()
        except:
            result = str(parameter.getValue())
            
    #        if type(parameter.getValue()) == int or type(parameter.getValue()) == float: 
        if parameter.getUnit() != '':
            return parameter.longName + ' = %s' % result + parameter.getUnit() + ''
        else:
            return parameter.longName + ' = %s' % result
    #        else:
    #            return parameter.longName + ' = %s ' % parameter.getValue()

###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################
