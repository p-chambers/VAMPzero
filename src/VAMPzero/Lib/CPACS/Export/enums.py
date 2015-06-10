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

class WING_LOD:
    '''
    Level of Detail for the wing export (use as ENUMS)
    -0 no export
    -1 single trapezoid wing
    -2 double trapezoid wing
    -3 advanced double trapezoid wing
    -4 UCAV
    -5 SBW
    -6 STRUT
    @author: Jonas Jepsen
    '''
    NONE, SINGLE, DOUBLE, ADVDOUBLE, UCAV, SBW, STRUT = range(7)

class FUSE_LOD:
    '''
    Level of Detail for the fuselage export (use as ENUMS)
    -0 no export
    -1 Cylinder
    -2 A320 scaled
    @author: Jonas Jepsen
    '''
    NONE, ZYL, A320 = range(3)
