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



zeroColor  = {
"aircraft"      :   [61,108,164],
"wing"          :   [60.,128,147],
"fuselage"      :   [255,140,0],
"engine"        :   [164,50,75],
"atmosphere"    :   [186,186,186],
"vtp"           :   [106,161,181],
"htp"           :   [157,195,208],
"fuel"          :   [60,179,113],
"systems"       :   [131,131,131],
"airfoil"       :   [202,223,226],
"pylon"         :   [218,138,131],
"landingGear"   :   [131,131,131],
"payload"       :   [139,91,65]
}

def toHEX(colour):
    '''
    Takes a RGB Color Code and converts it to a HEX Notation
    '''
    r = colour[0]
    g = colour[1]
    b = colour[2]
    return "#%02X%02X%02X" % (r, g, b)

def giveColorForNetworkx(colorList):
    '''
    Normalise Color List by 255.
    '''
    colors = []
    for item in colorList:
        colors.append(item / 255.)
    colors.append(1.)

    return  colors
