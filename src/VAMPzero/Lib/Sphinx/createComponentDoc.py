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
import inspect

def createComponentDoc(component,doc,components,disciplines,parentFolder):
    '''
    Creates the reStrucutredText documentation for a component
    it lists all nested disciplines and component.
    If the cpacsExport method of the component was overwritten
    it also posts a documentation for this. The doc file is saved in the
    parent Folder
    '''
    components  = sorted(components, key=str)
    disciplines = sorted(disciplines, key=str)
    
    componentName   = component.id
    fileName        = parentFolder+componentName+'.rst'
    className       = 'VAMPzero.Component.'+componentName.capitalize()+'.'+componentName+'.'+componentName
    
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
    out= ["Component: " + componentName.capitalize() + "\n",
          "=====================================\n",
          "\n",
          doc + "\n",
          "\n"]

    #===========================================================================
    # Included Disciplines
    #===========================================================================
    if disciplines:
        out.append("Included Disciplines\n")
        out.append("^^^^^^^^^^^^^^^^^^^^^^^^\n")
        out.append("\n")
        out.append(".. toctree::\n")
        out.append("   :maxdepth: 1\n")
        out.append("   \n")
        for name in disciplines:
            if componentName.lower() != name.lower():
                out.append('   '+name+'<'+name+'>\n')
        out.append("   \n")
        
    #===========================================================================
    # Nested Components
    #===========================================================================
    if components:
        out.append("Nested Components\n")
        out.append("^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        out.append("\n")
        out.append(".. toctree::\n")
        out.append("   :maxdepth: 1\n")
        out.append("   \n")
        for name in components:
            name = name.id
            out.append('   '+name.capitalize()+'<'+name+'/'+name+'>\n')
            
    #===========================================================
    # CPACS Export
    # If you do find that cpacsExport was overwritten print the methods doc
    #===========================================================
    out.append("   \n")
    if str(inspect.getmodule(component.cpacsExport)).find('Handler.Component')==-1: 
        out.append("CPACS Export"+'\n')
        out.append('^^^^^^^^^^^^^^^^^^^^^^^^^^\n')          
        out.append(".. automethod:: "+className+".cpacsExport"+'\n')    
        out.append('\n')
                
        
    myFile.writelines(out)
    myFile.close()