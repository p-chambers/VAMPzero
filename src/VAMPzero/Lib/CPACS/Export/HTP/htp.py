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

from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createWingWingAttachment

from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath, createTransformation, createHeader
from VAMPzero.Lib.CPACS.Export.Wing.Shape.trapezoid import createTrapezoidWing
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD
from VAMPzero.Lib.CPACS.cpacs import stringBaseType, stringUIDBaseType

def createHTP(CPACSObj, id, xRoot, zRoot, tcRoot, tcTip, cRoot, cTip, span, phiLE, dihedral, LoD=0, location=True):
    if LoD == WING_LOD.NONE:
        return 
    # just for now
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + id + ']'
    # the next line is the one to use later on
    # cpacsPath = '/cpacs/vehicles/aircraft/model[model]/wings/wing[' + self.id + ']'
    # get the wing object from given cpacs path
    myWing = getObjfromXpath(CPACSObj, cpacsPath)
    myWing.set_name(stringBaseType(valueOf_='htp'))
    strUID = createHeader(myWing, id)
    myWing.set_symmetry('x-z-plane')


    if location:
        myWing.set_parentUID(stringUIDBaseType(isLink=True, valueOf_='fuselage'))
        createTransformation(myWing, 'absGlobal', xRoot, 0., zRoot)
    else:
        myWing.set_parentUID(stringUIDBaseType(isLink=True, valueOf_='vtp'))
        createTransformation(myWing, 'absGlobal', xRoot, 0., zRoot)

    # call corresponding wing creation method
    if LoD == WING_LOD.SINGLE:
        createTrapezoidWing(myWing, id, tcTip, tcRoot, cTip, cRoot, span, phiLE, dihedral, 0., strUID)

    if not location:
        createWingWingAttachment(myWing.get_componentSegments().get_componentSegment()[0], strUID, targetUID='vtp_Cseg', typeOfSeg='ttail')
