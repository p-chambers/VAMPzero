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
from setuptools import setup, find_packages
from VAMPzero import version as VAMPversion

setup(
    name = "VAMPzero",
    version = VAMPversion,
    author = "Daniel Boehnke",
    author_email = "daniel.boehnke@dlr.de",
    description = ("VAMPzero is a software tool for the conceputal design of aircraft. \
                    Based on well known handbook methods the design of new configurations \
                    includes outer geometry as well as structures, engines, systems, mission \
                    analysis and costs. It supports working in multi-disciplinary and \
                    multi-fidelity environments. VAMPzero can interpret data from CPACS. \
                    Even more important VAMPzero can be used to generate CPACS files. \
                    Due to the fact that VAMPzero is based on an object oriented structure \
                    it is highly flexible. Furthermore, the structure distinguishes feature \
                    aspects (file handling, convergence control, process control) and design \
                    aspects (parameter definition, calculation methods) in a way that makes\
                     extensions easy to implement. The design aspects are grouped into components,\
                      disciplines and parameters, where as the parameters contain the actual design knowledge."),

    license = "Apache 2.0",
    keywords = "Aircraft Conceptual Design Multi-Fidelity",
    url = "http://vampzero.googlecode.com",
    packages=find_packages(),
    #List of the required packages
    #I left pySide out, because VAMPzero's own GUI isn't ready yet and the installer
    #seems to be bitching around with the installation of PySide
    install_requires=['setuptools>=0.6',
                      'matplotlib>=1.0',
                      'scipy>=0.9',
                      'numpy>=1.0',
                      'lxml>=2.1'],

)
