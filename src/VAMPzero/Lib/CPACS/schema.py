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

class toolSpecificSchema(object):
    '''
    Class that holds and creates the toolspecific block of the VAMPzero CPACS Schema
    '''
    def __init__(self,zeroTree,prefix=''):
        self.log    = zeroLogger('SchemaHandler')

        self.out    = []

        self.log.info('VAMPzero SCHEMA Created an object of toolSpecificSchema')
        self.log.info('VAMPzero SCHEMA Starting to create toolSpecificSchema')

        self.convertZeroTree(zeroTree, prefix)
         
    
    def createToolType(self,prefix=''):
        '''
        overall VAMPzero tooltype
        '''
        self.out.append('<xsd:complexType name="zeroToolType">')
        self.out.append('    <xsd:annotation>')
        self.out.append('        <xsd:appinfo>zeroToolType</xsd:appinfo>')
        self.out.append('        <xsd:documentation>VAMPzero tool type, containing VAMPzero tool data</xsd:documentation>')
        self.out.append('    </xsd:annotation>')
        self.out.append('    <xsd:complexContent>')
        self.out.append('        <xsd:extension base="complexBaseType">')
        self.out.append('            <xsd:sequence>')
        self.out.append('                <xsd:element name="tool" type="toolType">')
        self.out.append('                    <xsd:annotation>')
        self.out.append('                        <xsd:documentation>Tool identification</xsd:documentation>')
        self.out.append('                     </xsd:annotation>')
        self.out.append('                </xsd:element>')
        self.out.append('                <xsd:element name="aircraftModelUID" type="stringBaseType" />')
        self.out.append('                <xsd:element name="wingUID" type="stringBaseType" />')
        self.out.append('                <xsd:element name="vtpUID" type="stringBaseType" />')
        self.out.append('                <xsd:element name="htpUID" type="stringBaseType" />')        
        self.out.append('                <xsd:element name="engineUID" type="stringBaseType" />')    
        self.out.append('                <xsd:element name="components" type="'+prefix+'ComponentsType"/>')    
        self.out.append('            </xsd:sequence>')
        self.out.append('        </xsd:extension>')
        self.out.append('    </xsd:complexContent>')
        self.out.append('</xsd:complexType>')

        self.log.info('VAMPzero SCHEMA Created ToolType')

        return self.out
        

    
    def createSingularType(self,name,pluralChild,prefix=''):
        '''
        creates a SingularType
        '''     
        self.out.append('<xsd:complexType name=\"'+prefix+name+'Type\">')
        self.out.append('    <xsd:annotation>')
        self.out.append('        <xsd:appinfo>'+prefix+name+'Type</xsd:appinfo>')
        self.out.append('        <xsd:documentation>'+prefix+name+'Type</xsd:documentation>')
        self.out.append('    </xsd:annotation>')
        self.out.append('    <xsd:complexContent>')
        self.out.append('        <xsd:extension base="complexBaseType">')
        self.out.append('            <xsd:sequence>')
        self.out.append('                <xsd:element name="name" type="stringBaseType" />')        
        self.out.append('                <xsd:element name="description" type="stringBaseType" />')
        self.out.append('                <xsd:element name="'+pluralChild.lower()+'" type="'+prefix+pluralChild+'Type" minOccurs="0"/>')
        self.out.append('            </xsd:sequence>')
        self.out.append('        </xsd:extension>')
        self.out.append('    </xsd:complexContent>')
        self.out.append('</xsd:complexType>')

        self.log.info('VAMPzero SCHEMA Created SingularType: %s'%str(prefix+name))
        
        return self.out    

    def createPluralType(self,name,singularChild,prefix=''):
        '''
        creates a PluralType
        '''     
        self.out.append('<xsd:complexType name=\"'+prefix+name+'Type\">')
        self.out.append('    <xsd:annotation>')
        self.out.append('        <xsd:appinfo>'+prefix+name+'Type</xsd:appinfo>')
        self.out.append('        <xsd:documentation>'+prefix+name+'Type</xsd:documentation>')
        self.out.append('    </xsd:annotation>')
        self.out.append('    <xsd:complexContent>')
        self.out.append('        <xsd:extension base="complexBaseType">')
        self.out.append('            <xsd:sequence>')
        self.out.append('                <xsd:element name="'+singularChild.lower()+'" type="'+prefix+singularChild+'Type" minOccurs="1" maxOccurs="unbounded"  />')
        self.out.append('            </xsd:sequence>')
        self.out.append('        </xsd:extension>')
        self.out.append('    </xsd:complexContent>')
        self.out.append('</xsd:complexType>')

        self.log.info('VAMPzero SCHEMA Created PluralType: %s'%str(prefix+name))
        
        return self.out    

    
    def createParameterType(self,prefix = ''):
        '''
        base VAMPzero parameter type
        '''
        self.out.append('<xsd:complexType name=\"'+prefix+'ParameterType\">')
        self.out.append('    <xsd:annotation>')
        self.out.append('        <xsd:appinfo>'+prefix+'Parameter</xsd:appinfo>')
        self.out.append('        <xsd:documentation>'+prefix+'Parameter</xsd:documentation>')
        self.out.append('    </xsd:annotation>')
        self.out.append('    <xsd:complexContent>')
        self.out.append('        <xsd:extension base="complexBaseType">')
        self.out.append('            <xsd:all>')
        self.out.append('                <xsd:element name=\"name\" type=\"stringBaseType'+'\"/>')
        self.out.append('                <xsd:element name=\"value\" type=\"doubleBaseType'+'\"/>')
        self.out.append('                <xsd:element name=\"factor\" type=\"doubleBaseType\"/>')
        self.out.append('            </xsd:all>')
        self.out.append('        </xsd:extension>')
        self.out.append('    </xsd:complexContent>')
        self.out.append('</xsd:complexType>')
        self.log.info('VAMPzero SCHEMA Created ParameterType')
        
        return self.out
    

    def convertZeroTree(self,zeroTree,prefix=''):
        '''
        convert a zeroTree to toolspecific input schema for cpacs
        prefix is used to adjust prefix!
        '''
#        components  = []
        self.createToolType(prefix)
        self.createPluralType('Components', 'Component', prefix)
        self.createSingularType('Component', 'Disciplines', prefix)                
        self.createPluralType('Disciplines', 'Discipline', prefix)
        self.createSingularType('Discipline', 'Parameters', prefix)
        self.createPluralType('Parameters', 'Parameter', prefix)
        self.createParameterType(prefix)
    
            
        myFile  = open('./VAMPzero/Lib/CPACS/CPACSxml/toolSpecific.xsd','w')
        myFile.writelines(self.out)
        myFile.close()
        self.log.info('VAMPzero SCHEMA Saved toolspecific schema to ./toolSpecific.xsd')        
        return self.out

def printZeroTree(zeroTree):
    '''
    Prints a zeroTree as created in cpacsDoc
    '''
    myFile = open('./VAMPzero/Lib/GUI/guiIn.xml','w')
    
    out    = ['<?xml version="1.0" encoding="UTF-8"?>', '<zeroGuiIn>']

    for item in zeroTree.items():
        componentName     = item[0].capitalize()
        out.append( '<component>')
        out.append(  '<name>'+componentName+'</name>')
        out.append( '<disciplines>')
        for discipline in item[1].items():
            disciplineName = discipline[0].capitalize()
            if cmp(disciplineName,componentName):       
                out.append( '    <discipline>')
                out.append(  '        <name>'+disciplineName+'</name>')
                out.append( '         <parameters>')
                for parameter in discipline[1]:
                    parameterName = parameter["name"]
                    out.append( '        <parameter>')
                    out.append( '            <name>'+parameterName+'</name>')
                    out.append( '            <description>'+str(parameter['doc'])+'</description>')
                    out.append( '            <value>0.0</value>')
                    out.append( '            <factor>1.0</factor>')
                    out.append( '        </parameter>')
                out.append( '         </parameters>')
                out.append( '    </discipline>')
        out.append( '</disciplines>')
        out.append( '</component>')
    out.append('</zeroGuiIn>')
    myFile.writelines(out)

    myFile.close()
    
def printZeroTreeToSphynx(zeroTree):
    '''
    Prints a zeroTree as created in cpacsDoc
    '''
    components = []

    for item in zeroTree.items():
        componentName     = item[0].capitalize()
        components.append(componentName)
        disciplines = []
        
        for discipline in item[1].items():
            disciplineName = discipline[0].capitalize()
            disciplines.append(disciplineName)
            parameters = []
            
            if cmp(disciplineName,componentName):
                for parameter in discipline[1]:
                    parameterName = parameter["name"]
                    parameters.append(parameterName)

            
            disciplineFile(componentName, disciplineName, parameters)
        
        
        componentFile(componentName, disciplines)
                    
    
    componentsFile(components)
###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################