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

import unittest
from VAMPzero import Vampzero


class VAMPzeroConfigurationTests(unittest.TestCase):
    
    def test_A320_JTI(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A320_JTI.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)
    
#     def test_A320Neo_JTI(self):
#         vampzero = Vampzero(cpacsIn='./TestData/A320Neo_JTI.xml')
#         exitcode = vampzero.run()
#         self.assertEqual(exitcode, 0)

    def test_A300_600(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A300-600.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A310_300(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A310-300.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A310_308(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A310-308.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A318_100(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A318-100.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A319_100(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A319-100.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A320_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A320-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A321_100(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A321-100.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A330_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A330-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A330_300(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A330-300.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A340_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A340-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A340_500(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A340-500.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A340_600(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A340-600.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_A380_800(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/A380-800.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B707_320(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B707-320.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B707_320C(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B707-320C.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B717_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B717-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B737_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B737-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B737_400(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B737-400.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B737_500(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B737-500.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B737_700(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B737-700.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B737_800(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B737-800.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B737_900(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B737-900.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B747_400(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B747-400.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B757_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B757-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B757_300(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B757-300.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B767_200(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B767-200.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B767_200ER(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B767-200ER.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B767_300(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B767-300.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B767_300ER(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B767-300ER.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)

    def test_B777_200ER(self):
        vampzero = Vampzero(cpacsIn='./TestData/aircraft/B777-200ER.xml')
        exitcode = vampzero.run()
        self.assertEqual(exitcode, 0)


