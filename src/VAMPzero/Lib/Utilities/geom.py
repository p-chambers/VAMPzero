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
def calc_trapezoidCenterOfArea(xa, ya, ca, xb, cb, dy):
    '''
    @param xa: x coordinate of inner chord
    @param ya: y coordinate of inner chord
    @param ca: chord length of inner chord
    @param xb: x coordinate of outer chord
    @param cb: chord length of outer chord
    @param dy: distance in y direction between the two chords
    '''
    xeta = (xb + cb) - xa
    xs = xa + (ca**2 - cb**2 + xeta*(ca + 2. * cb)) / (3. * (ca + cb))
    ys = ya + dy / 3. * (ca + 2. * cb) / (ca + cb)
    return (xs, ys)

def calc_chord(cRoot, span, taperRatio, y):
    '''
    Calculates the chord length at a given y-coordinate point.
    A simple interpolation of chord length.
    '''
    return cRoot * (1 - y / (span / 2.) * (1 - taperRatio))

#def calc_tankCoG(xa, ya, ca, xb, cb, dy):
#    xa = 
#    pass