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
from VAMPzero.Lib.CPACS.Export.Wing.Shape.strut import createStrut
from VAMPzero.Lib.CPACS.Export.Wing.Shape.strutbracedwing import createStrutBracedWing

from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath, createTransformation, createHeader
from VAMPzero.Lib.CPACS.Export.Wing.Shape.trapezoid import createTrapezoidWing
from VAMPzero.Lib.CPACS.Export.Wing.Shape.doubletrapezoid import createDoubleTrapezoidWing
from VAMPzero.Lib.CPACS.Export.Wing.Shape.advDoubletrapezoid import createAdvDoubleTrapezoidWing
from VAMPzero.Lib.CPACS.Export.Wing.Shape.ucav import createUCAVWing
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD
from VAMPzero.Lib.CPACS.cpacs import stringUIDBaseType, stringBaseType


def createWing(CPACSObj = None, zeroWing = None, id="1", LoD = 0.):
    """
    This function triggers the different export modes of the wing depending on the desired
    level of detail.

    Options include a single trapezoid, double trapezoid, advanced double trapezoid (that includes
    a rectangular center fuselage section) and a strut-braced wing.

    Please note, these are the internal guts of VAMPzero's CPACS export. A lot of the code
    here is experimental and furthermore highly chaotic. In case of emergency contact Daniel or Jonas.

    :param CPACSObj: The overall CPACS object of the export
    :param zeroWing: The instance of the wing.
    :param id: The id of the wing, mostly sth. like wing
    :param LoD: The level of detail of the desired input.
    :return: CPACSObj including a new wing
    """
    if LoD == WING_LOD.NONE:
        return 
    # just for now
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + id + ']'
    # the next line is the one to use later on
    # cpacsPath = '/cpacs/vehicles/aircraft/model[model]/wings/wing[' + self.id + ']'
    # get the wing object from given cpacs path
    cpacsWing = getObjfromXpath(CPACSObj, cpacsPath)
    strUID = createHeader(cpacsWing, id)
    
    cpacsWing.set_symmetry('x-z-plane')
    cpacsWing.set_name(stringBaseType(valueOf_='wing'))
    cpacsWing.set_parentUID(stringUIDBaseType(isLink=True, valueOf_='fuselage'))
    

    xRoot = zeroWing.xRoot.getValue()
    zRoot = zeroWing.zRoot.getValue()
    cRoot = zeroWing.cRoot.getValue()
    cTip = zeroWing.cTip.getValue()
    span = zeroWing.span.getValue()
    dfus = zeroWing.aircraft.fuselage.dfus.getValue()
    phiLE = zeroWing.phiLE.getValue()
    dihedral = zeroWing.dihedral.getValue()
    twist = zeroWing.twist.getValue()
    Sref = zeroWing.refArea.getValue()
    xMAC25 = zeroWing.xMAC25.getValue()
    tcRoot = zeroWing.airfoilr.tc.getValue()
    tcTip = zeroWing.airfoilt.tc.getValue()

    try:
        etakf = zeroWing.etaKink.getValue()
        yFus = zeroWing.yFuselage.getValue()
        etaEng = zeroWing.etaEngine.getValue()
        etaFus = yFus/span*2.
    except AttributeError:
        pass #As not all components that call this method have a kink

    try:
        yRoot = zeroWing.yRoot.getValue()
    except AttributeError:
        pass #As not all components that call this method have a kink



    createTransformation(cpacsWing, 'absGlobal', xRoot, 0., zRoot)
    # call corresponding wing creation method
    if LoD == WING_LOD.SINGLE:
        createTrapezoidWing(cpacsWing, id, tcRoot, tcTip, cTip, cRoot, span, phiLE, dihedral, twist, strUID)
    elif LoD == WING_LOD.DOUBLE:
        createDoubleTrapezoidWing(cpacsWing, id, cTip, cRoot, span, Sref, phiLE, dihedral, twist, xMAC25, etakf, strUID)
    elif LoD == WING_LOD.ADVDOUBLE:
        createAdvDoubleTrapezoidWing(cpacsWing, id, cTip, cRoot, span, Sref, dfus, phiLE, dihedral, twist, xMAC25, etakf, strUID, yFus, xRoot, etaEng, tcRoot, tcTip)
    elif LoD == WING_LOD.UCAV:
        createUCAVWing(cpacsWing, id, cTip, cRoot, span, Sref, phiLE, dihedral, etakf, strUID)
    elif LoD == WING_LOD.SBW:
        print "dihedral", dihedral
        etaStrut = zeroWing.aircraft.strut.etaStrut.getValue()
        createStrutBracedWing(cpacsWing, id=id, cTip=cTip, cRoot=cRoot, span=span, Sref=Sref, phiLE=phiLE, dihedral=dihedral, twist=twist, xMAC25=xMAC25, etaFus=etaFus, etaStrut=etaStrut, tcRoot=tcRoot, tcTip=tcTip, xRoot=xRoot, strUID=strUID)
    elif LoD == WING_LOD.STRUT:
        etaStrut = zeroWing.aircraft.strut.etaStrut.getValue()
        createStrut(cpacsWing, id=id, cTip=cTip, cRoot=cRoot, span=span, phiLE=phiLE, dihedral=dihedral, tcRoot=tcRoot, tcTip=tcTip, xRoot=xRoot, yRoot=yRoot, twist=twist, etaStrut=etaStrut,  strUID=strUID)
