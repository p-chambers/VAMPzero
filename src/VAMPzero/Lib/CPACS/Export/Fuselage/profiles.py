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

from math import pi, sin, cos

SQUARE = [
          [1.,1.],
          [-1.,1.],
          [-1.,-1.],
          [1.,-1.],
          [1.,1.],
          ]
# #################
# FUSELAGE
# #################
# ellipse data[x_rel,z-dist,height/2,width/2]
NOSE = [
        [0.00000, -0.17478, 0.00000, 0.00000],
        [0.00952, -0.17908, 0.06590, 0.08051],
        [0.02377, -0.17709, 0.10426, 0.12253],
        [0.03797, -0.17606, 0.13204, 0.14861],
        [0.05584, -0.17363, 0.16088, 0.17544],
        [0.06413, -0.17226, 0.17226, 0.18709],
        [0.07602, -0.17138, 0.18601, 0.20177],
        [0.09620, -0.16882, 0.20647, 0.22354],
        [0.11875, -0.16676, 0.22534, 0.24354],
        [0.14493, -0.16484, 0.24501, 0.26759],
        [0.17515, -0.16090, 0.26256, 0.29266],
        [0.19717, -0.15027, 0.28273, 0.30734],
        [0.22211, -0.13938, 0.30342, 0.32405],
        [0.25057, -0.12068, 0.33079, 0.34076],
        [0.27551, -0.10623, 0.35346, 0.35443],
        [0.30405, -0.09150, 0.37688, 0.36810],
        [0.33849, -0.07770, 0.39829, 0.38380],
        [0.38485, -0.06390, 0.42163, 0.40253],
        [0.44422, -0.05220, 0.44415, 0.42354],
        [0.51189, -0.04283, 0.46308, 0.44557],
        [0.57956, -0.03523, 0.47606, 0.46127],
        [0.65560, -0.02996, 0.48341, 0.47595],
        [0.75419, -0.02523, 0.49245, 0.48937],
        [0.83489, -0.02344, 0.49645, 0.49696],
        [0.88838, -0.02253, 0.49847, 0.50000],
        [0.94660, -0.02252, 0.49944, 0.50000],
        [1.00000, -0.02306, 0.50000, 0.50000]
        ]

CABIN = [
            [0.00000, -0.02306, 0.50000, 0.50000],
            [0.20000, -0.02306, 0.50000, 0.50000],
            [0.40000, -0.02306, 0.50000, 0.50000],
            [0.60000, -0.02306, 0.50000, 0.50000],
            [0.80000, -0.02306, 0.50000, 0.50000],
            [1.00000, -0.02306, 0.50000, 0.50000]
          ]
TAIL = [
          [0.00000, -0.02306, 0.50000, 0.50000],
          [0.05920, -0.02307, 0.50000, 0.50000],
          [0.09581, -0.02263, 0.49957, 0.50000],
          [0.13249, -0.02019, 0.49713, 0.50000],
          [0.16909, -0.01620, 0.49314, 0.50000],
          [0.20570, -0.01064, 0.48758, 0.50000],
          [0.24238, -0.00368, 0.48062, 0.50000],
          [0.27898, 0.00418, 0.47211, 0.49949],
          [0.31566, 0.01290, 0.46221, 0.49620],
          [0.35227, 0.02230 ,0.45097, 0.48810],
          [0.39238, 0.03341, 0.43732, 0.47765],
          [0.43894, 0.04522, 0.42259, 0.46003],
          [0.50275, 0.06665, 0.39515, 0.42084],
          [0.53544, 0.07859, 0.37941, 0.40089],
          [0.57617, 0.09242, 0.36047, 0.37213],
          [0.60130, 0.10111, 0.34839, 0.35359],
          [0.63228, 0.11192, 0.33310, 0.32886],
          [0.65975, 0.12159, 0.31917, 0.30509],
          [0.68723, 0.13135, 0.30490, 0.28481],
          [0.71559, 0.14145, 0.28975, 0.26159],
          [0.74396, 0.15159, 0.27415, 0.24109],
          [0.77232, 0.16391, 0.25580, 0.22795],
          [0.82418, 0.18068, 0.22147, 0.20886],
          [0.89286, 0.19932, 0.17368, 0.18380],
          [0.92720, 0.20964, 0.14588, 0.17405],
          [0.96154, 0.22134, 0.11670, 0.15316],
          [0.97871, 0.22659, 0.09981, 0.13367],
          [0.99995, 0.22986, 0.08487, 0.09494],
          [1.00000, 0.23306, 0.00000, 0.00000]
        ]

def createCircleList():
    xList = []
    yList = []
    zList = []
    n=80
    for i in range(0,n+1):
        x = 0.0
        z = sin(360.0 * i / float(n) / 180.0 * pi)
        y = cos(360.0 * i / float(n) / 180.0 * pi)
        z=round(z,10)
        y=round(y,10)
        
        xList.append(str(x))
        yList.append(str(y))
        zList.append(str(z))
        
    return xList, yList, zList