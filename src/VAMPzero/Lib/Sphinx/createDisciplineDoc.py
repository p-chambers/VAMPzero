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

def createDisciplineDoc(disciplines, parentFolder):
    '''
    Creates y discipline files in the parentFolder
    Each discipline links to the adjacent parameters
    '''
    def createDoc(disciplineName,parameters,parentFolder):
        '''
        creates a discipline doc file
        '''
        parameters      = sorted(parameters, key=str)
        fileName        = parentFolder+disciplineName+'.rst'
        
        #==============================================================================
        #Create Folder and File 
        #==============================================================================
        dir = os.path.dirname(fileName)

        if not os.path.exists(dir):
            os.makedirs(dir)

        myFile  = file(fileName,'w')

        #===========================================================================
        # Header
        #===========================================================================
        out= ['.. _' + parentFolder.split('//')[0].split('/')[-2] + '.' + disciplineName + ':\n',
              '\n',
              "Discipline: " + disciplineName + "\n",
              "---------------------------------------\n",
              "\n",
              ".. toctree::\n",
              "   :maxdepth: 1\n",
              "   \n"]


        for name in parameters:
            out.append('   '+name+'<'+name+'/'+name+'>\n')
            
        myFile.writelines(out)
        myFile.close()
    
    for discipline in disciplines:
        createDoc(discipline,disciplines[discipline],parentFolder)
    
    
