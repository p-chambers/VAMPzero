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
 
import networkx
import matplotlib.pyplot as plt
from VAMPzero.Lib.Log.log import zeroLogger
from VAMPzero.Lib.Colors.colors import giveColorForNetworkx, zeroColor


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

class zeroGraph(object):
    
    def __init__(self):
        self.graph  = networkx.Graph()
        self.log    = zeroLogger('Graph')
        
    def addNode(self,parameter,propList):
        
        self.graph.add_node(parameter, color = chooseColor(parameter))
        propList["colors"].append(chooseColor(parameter))
        propList["labels"].append('')
        self.log.info('VAMPzero GRAPH: adding Node: %s' %parameter)

        return propList

    def createEdges(self,edgeList):

        for item in edgeList:
            self.graph.add_edge(item[0],item[1])
            if item[0].split('.')[0]==item[1].split('.')[0]:
                self.graph.edge[item[0]][item[1]]['weight'] = 10
            self.log.info('VAMPzero GRAPH: adding Edge between: %s and %s' %(item[0],item[1]))
            
    def draw(self,node_color,fixList):
        #pos = networkx.spring_layout(self.graph,dim=2, weighted = True, iterations = 1000, pos = fixList, fixed = fixList.keys(), scale = 1.)
        pos = networkx.circular_layout(self.graph,dim=2)
        #pos = networkx.spectral_layout(self.graph,dim=2)
        
        node_color = []
        for node in self.graph.nodes(data = True):
            try:
                node_color.append(node[1]["color"])
                
            except:
                node_color.append(chooseColor(node[0]))

        networkx.draw(self.graph,node_color = node_color,pos = pos,font_size =2, node_shape='o',with_labels=False, edge_color= '0.5',node_size = 90)
        

        plt.show()


def chooseColor(name):
    '''
    find a descent color from a containing string
    '''
    if name.find("payload") != -1:
        return giveColorForNetworkx(payloadC)
    elif name.find("aircraft") != -1:
        return giveColorForNetworkx(aircraftC)
    elif name.find("wing") != -1:
        return giveColorForNetworkx(wingC)
    elif name.find("fuselage") != -1:
        return giveColorForNetworkx(fuselageC)
    elif name.find("engine") != -1:
        return giveColorForNetworkx(engineC)
    elif name.find("atmosphere") != -1:
        return giveColorForNetworkx(atmosphereC)
    elif name.find("vtp") != -1:
        return giveColorForNetworkx(vtpC)
    elif name.find("htp") != -1:
        return giveColorForNetworkx(htpC)
    elif name.find("fuel") != -1:
        return giveColorForNetworkx(fuelC)
    elif name.find("systems") != -1:
        return giveColorForNetworkx(systemsC)
    elif name.find("airfoil") != -1:
        return giveColorForNetworkx(airfoilC)
    elif name.find("pylon") != -1:
        return giveColorForNetworkx(pylonC)
    elif name.find("landingGear") != -1:
        return giveColorForNetworkx(landingGearC)
    else:
        return 'k'