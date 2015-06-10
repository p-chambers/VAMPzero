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


class outMapping(object):
    '''
    Class for generating mapping files from the cpacsPaths already defined in VAMPzero
    @todo: mapping: all parameters that have their own cpacsImport export method need to have a cpacsPath to the highest node
    '''
    def __init__(self, component):
        self.log        = zeroLogger('outMapping')
        
        self.log.info('VAMPzero MAP: Created an Instance of outMapping')
        self.log.info('VAMPzero MAP: Creating mappingOut.xml')
        self.createMapping(component)
    
    def createMapping(self, component):
        '''
        opens a file for writing and outputs classic mapping style 
        '''
        myFile = open("mappingOutput.xml",'w')
        myFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        myFile.write("<map:mappings xmlns:map=\"http://www.dlr.de/sistec/tiva/tool/mapping\" xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\">\n")
        
        component.createMapping(myFile)
        
        myFile.write("</map:mappings>\n")
        
        myFile.close()
        
        self.log.info('VAMPzero MAP: Created mappingOut.xml')

