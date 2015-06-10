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
'''
from distutils.core import setup
import py2exe
import matplotlib
import sys

import pylab

#This is the setup file for the binary release of VAMPzero

setup(console=[{"script":'VAMPzeroCPACS.py',"icon_resources":[(0,"VAMPzero.ico")]}],
      zipfile="./shared/library.zip",
      options={"py2exe": {"bundle_files":3,
                          "compressed":True,
                          "dist_dir":"bin",
                          "packages":["matplotlib", "pytz", "lxml", "gzip", "scipy"],
                          "excludes":['_ssl', 'pyreadline', 'doctest', 'optparse'],
                          'includes': ['scipy.sparse.csgraph._validation'],
                          "dll_excludes": ['libgobject-2.0-0.dll',
                                           'libgdk-win32-2.0-0.dll',
                                           'libgdk_pixbuf-2.0-0.dll']}},
      data_files=matplotlib.get_py2exe_datafiles())
