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
import sys

def createParameterDoc(thisParameter,myAircraft,parentFolder):
    '''
    Creates a restructured Text file for the documentation of
    a single parameter. It takes into account the parameters
    doc-string, all implemented calc methods and cpacsImport and
    cpacsExport methods. If cpacsImport and cpacsExport are overwritten
    from the parent class (parameter) their docstrings are specified. As
    alternative the cpacsPath is displayed.
    '''
    
    def prettyPrintXPath(out,path):
        '''
        Takes an XPath and converts it into several lines.
        Indentation is also applied so that the readability of
        the documentation is increased
        '''
        items = path.split('/')
        items.pop(0)
        i     =1
        out.append('\n')
        out.append('.. code-block:: xml\n')
        out.append('\n')
        for item in items:
            out.append(i*3*' '+'<'+item+'>\n')
            i+=1
        return out
    #=======================================================================
    # Catch Names
    #=======================================================================
    parameterName   = thisParameter["name"]
    
    fileName        = parentFolder+parameterName+'/'+parameterName+'.rst'
    className       = str(inspect.getmembers(thisParameter)[0][1]).split('\'')[1]
    
    ownImportMethod  = False
    ownExportMethod  = False
    
    #=======================================================================
    #Create Folder and File 
    #=======================================================================
    if not os.path.exists(os.path.dirname(fileName)):
        os.makedirs(os.path.dirname(fileName))
    
    myFile  = file(fileName,'w')

    #===========================================================================
    # Header
    #===========================================================================
    out= ['.. _' + parentFolder.split('//')[0].split('/')[-2] + '.' + parameterName + ':\n',
          '\n',
          "Parameter: " + parameterName + '\n',
          '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n',
          thisParameter.__doc__ + '\n',
          '\n',
          "Calculation Methods" + '\n',
          '"""""""""""""""""""""""""""""""""""""""""""""""""""""""\n']

    #=======================================================================
    # Calc Methods
    #=======================================================================

    for para in dir(thisParameter):
        if str(para).find("calc")!=-1:
            out.append(".. automethod:: "+className+"."+str(para)+'\n')
            out.append('\n')
            
            #Clean the callee
            thisParameter["callee"] = []
            
            thisParameter.picName = os.path.dirname(fileName)+'/'+str(para)+'.jpg'
            
            #get the calc Function and try to call it
            callFunction = getattr(thisParameter,para)
            try:
                thisParameter.calc = callFunction
                callFunction()
                thisParameter.complexify()
                thisParameter.sense(myAircraft, doc=True, name=str(para))
                
            except Exception, e:
                print "Unexpected error:", sys.exc_info()[0], e
                print "could not call function" , thisParameter.longName, para
            

            
            if thisParameter["callee"]:
                calleeList = '   :Dependencies: \n'
                for item in thisParameter["callee"]:
                    calleeList= calleeList +'   * :ref:`' +(item.longName+'`\n')
                
                out.append('\n')
                out.append(calleeList+'\n')
                out.append('\n')
                       
            if os.path.isfile(os.path.dirname(fileName)+'/'+str(para)+'.jpg'):
                out.append('   :Sensitivities: \n')
                out.append(".. image:: "+str(para)+'.jpg \n')
                out.append('   :width: 80% \n')
                out.append('\n')
            out.append('\n')
                
    #===========================================================
    # CPACS Import
    # If you do find that cpacsImport was overwritten print the methods doc
    # If this is not the case and a XPath is available print it
    #===========================================================
    if str(inspect.getmodule(thisParameter.cpacsImport)).find('Parameter')==-1: 
        out.append("CPACS Import"+'\n')
        out.append('"""""""""""""""""""""""""""""""""""""""""""""""""""""""\n')          
        out.append(".. automethod:: "+className+".cpacsImport"+'\n')    
        out.append('\n')
        ownImportMethod = True
    
    if thisParameter["cpacsPath"] != "" and not ownImportMethod:
        out.append("CPACS Import"+'\n')
        out.append('"""""""""""""""""""""""""""""""""""""""""""""""""""""""\n')
        out.append('The values for '+parameterName+' are imported from:\n')
        out = prettyPrintXPath(out, thisParameter["cpacsPath"])    
        out.append('\n')


    #===============================================================
    # CPACS Export 
    # If you do find that cpacsExport was overwritten print the methods doc
    # If this is not the case and a XPath is available print it
    #===============================================================
    if str(inspect.getmodule(thisParameter.cpacsExport)).find('Parameter')==-1: 
        out.append("CPACS Export"+'\n')
        out.append("-------------------"+'\n')          
        out.append(".. automethod:: "+className+".cpacsExport"+'\n')    
        out.append('\n')
        ownExportMethod = True

    if thisParameter["cpacsPath"] != "" and not ownExportMethod:
        out.append("CPACS Export"+'\n')
        out.append("-------------------"+'\n')
        out.append('The values for '+parameterName+' are exported to:\n')
        out = prettyPrintXPath(out, thisParameter["cpacsPath"])
        out.append('\n')

    myFile.writelines(out)
    myFile.close()
