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

def componentsFile(components):
    '''
    Creates the header components.rst File
    '''
    components = sorted(components, key=str)
    
    fileName        = './VAMPzero/doc/Components/components.rst'
    #==============================================================================
    #Create Folder and File 
    #==============================================================================
    dir = os.path.dirname(fileName)
    if not os.path.exists(dir):
        os.makedirs(dir)
    myFile  = file(fileName,'w')

    out= ["Components\n",
          "==========\n",
          "\n",
          "A component is the highest level class in VAMPzero. A component will hold several disciplines, where as each discipline is then grouped into different parameters. \n",
          "Components and disciplines are mostly used for the managment of the code. The design knowlegd itself is captured in the parameters.\n",
          "For the export to CPACS, components (e.g. wing) can hold additional methods\n\n",
          "\n",
          "This is a list of all components included in VAMPzero\n",
          "\n",
          ".. toctree::\n",
          "   :maxdepth: 1\n",
          "   \n"]

    for name in components:
        out.append("   "+name+'<'+''+name+'/'+name+'>\n')
        
    myFile.writelines(out)
    myFile.close()