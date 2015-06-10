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
from VAMPzero.Lib.CPACS.Export.enums import WING_LOD
from VAMPzero.Lib.CPACS.Export.export import getObjfromXpath
from VAMPzero.Lib.CPACS.cpacs import controlSurfaceBorderTrailingEdgeType, \
    leadingEdgeShapeType, doubleBaseType, trailingEdgeDeviceType, \
    controlSurfacesType, trailingEdgeDevicesType, controlSurfaceOuterShapeTrailingEdgeType, \
    stringBaseType, stringUIDBaseType, wingComponentSegmentStructureType
from VAMPzero.Lib.Log.log import zeroLogger
from math import pi, tan, sqrt, ceil
from types import NoneType
import scipy.interpolate
import sys
from VAMPzero.Handler.Parameter import parameter
from VAMPzero.Lib.CPACS.Export.Wing.Structure.functions import createShell, \
    createSpars, createRibs
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Track.track import createTracks
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.Path.path import createPath
from VAMPzero.Lib.CPACS.Export.Wing.ControlSurface.CruiseRoller.cruiseRoller import createCruiseRollers



rad = pi / 180.
log = zeroLogger('Flap')

def calcChordLengthAtEta(eta, parentWingVAMPzero, parentWingCPACS):
    '''
    A function to calculate the absolute length of the wings chord depending on the relative eta coordinate. 
    This function is valid for the export case of the adv double trapezoid wing
    The parentWingVAMPzero is a VAMPzero wing component, not a CPACS vile
    '''
    cRoot = eval(parentWingCPACS.get_sections().get_section()[0].get_transformation().get_scaling().get_x().valueOf_)
    cKink = eval(parentWingCPACS.get_sections().get_section()[2].get_transformation().get_scaling().get_x().valueOf_)
    cTip  = eval(parentWingCPACS.get_sections().get_section()[3].get_transformation().get_scaling().get_x().valueOf_)
    
    etaFus = parentWingVAMPzero.yFuselage.getValue() / parentWingVAMPzero.span.getValue() / 2.
    etaKink= parentWingVAMPzero.etaKink.getValue()
    # if eta lies at the fuselage than return cRoot
    if eta <= etaFus:
        return cRoot
    
    # elif eta lies in the inboard section do linear interpolation
    elif eta <= etaKink:
        chord = cRoot + (cKink - cRoot)/(etaKink-etaFus)*(eta-etaFus)
        return chord
    
    # elif eta lies in the outboard section do linear interpolation
    elif eta > etaKink  and eta < 1.:
        chord = cKink + (cTip - cKink)/(1.0-etaKink)*(eta-etaKink)
        return chord
    else:
        log.warning('VAMPzero CHORD: Calculation of chord at eta location called for invalid eta: %s' % str(eta))
        raise ValueError

def createFlaps(parentWingCPACS, parentWingVAMPzero, myFlap, typeOfSeg):
    if typeOfSeg == WING_LOD.SBW:
        return createFlapsSBW(parentWingCPACS=parentWingCPACS, parentWingVAMPzero=parentWingVAMPzero, myFlap=myFlap)
    elif typeOfSeg == WING_LOD.ADVDOUBLE:
        return createFlapsAdvDoubleTrapezoid(parentWingCPACS=parentWingCPACS, parentWingVAMPzero=parentWingVAMPzero, myFlap=myFlap)
    else:
        return parentWingCPACS

def createFlapsSBW(parentWingCPACS, parentWingVAMPzero, myFlap):
    '''
    This is the main export method for the wings flaps

    @todo: it is possible that the inner flap overlaps the kink area
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentWingVAMPzero.id + ']'
    cpacsWing = getObjfromXpath(parentWingCPACS, cpacsPath)
    cpacsComponentSegment = cpacsWing.get_componentSegments().get_componentSegment()[0]
    myFlaps = []

    #===========================================================================
    # Initialization, i.e. fetching values throughout the code
    #===========================================================================
    xsiSparRoot = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[3].get_xsi().valueOf_)
    xsiSparFuselage = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[4].get_xsi().valueOf_)
    xsiSparKink = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[5].get_xsi().valueOf_)
    xsiSparTip = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[6].get_xsi().valueOf_)

    etaSparRoot = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[3].get_eta().valueOf_)
    etaSparFuselage = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[4].get_eta().valueOf_)
    etaSparKink = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[5].get_eta().valueOf_)
    etaSparTip = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[6].get_eta().valueOf_)

    xsiSpar_interp = scipy.interpolate.interp1d([etaSparRoot, etaSparFuselage, etaSparKink, etaSparTip], [xsiSparRoot, xsiSparFuselage, xsiSparKink, xsiSparTip])

    yFus = parentWingVAMPzero.yFuselage.getValue()
    span = parentWingVAMPzero.span.getValue() / 2.
    etaFus = yFus / span
    etaKink = parentWingVAMPzero.etaKink.getValue()
    cRoot = parentWingVAMPzero.cRoot.getValue()
    cKink = calcChordLengthAtEta(etaKink, parentWingVAMPzero, cpacsWing)
    phiLE = parentWingVAMPzero.phiLE.getValue()

    innerFlapArea = myFlap.refAreaInnerFlap.getValue()
    outerFlapArea = myFlap.refAreaOuterFlap.getValue()



    #===========================================================================
    # OuterFlap
    #===========================================================================
    sparOffset = 0.08

    # maxX is the maximum extension of the flap
    maxX = cRoot * (1. - (xsiSparRoot + sparOffset)) /2.
    newOuterFlapArea = innerFlapArea + outerFlapArea
    cRootOuterFlap = cRoot * (1. - (xsiSparRoot + sparOffset))

    #===========================================================================
    # Determine the total flap span by iteration
    #===========================================================================
    calcArea = 0.
    spanOuterFlap = 0.
    absSparOffset = sparOffset * cKink

    # Obtain the maxEtaValue. This is forwarded from the ailerons export routine.
    maxEta = myFlap.maxEta.getValue() - 0.02

    # the tip root length is a function of the span (as the xsi location of the spar changes)
    while abs(calcArea - newOuterFlapArea) > 0.1:
        spanOuterFlap += .01
        cTipOuterFlap = calcChordLengthAtEta(etaFus + spanOuterFlap / span, parentWingVAMPzero, cpacsWing) * (1 - xsiSpar_interp(etaFus + spanOuterFlap / span)) - absSparOffset
        oldcalcArea = calcArea
        calcArea = spanOuterFlap * (cRootOuterFlap + cTipOuterFlap) / 2.

        if calcArea < oldcalcArea:
            log.warning('VAMPzero FLAP: Outer Flap Area can not be established decreasing spar offset by 2% chord!')
            sparOffset = sparOffset - 0.02
            calcArea = 0.
            spanOuterFlap = 0.
            absSparOffset = sparOffset * cKink
            break

        if spanOuterFlap / span + etaFus > maxEta:
            log.warning('VAMPzero FLAP: Outer Flap overlaps with the aileron decreasing spar offset by 2% chord!')
            sparOffset = sparOffset - 0.02
            calcArea = 0.
            spanOuterFlap = 0.
            absSparOffset = sparOffset * cRoot
            break


    while abs(calcArea - newOuterFlapArea) > 0.1:
        spanOuterFlap += .01
        cTipOuterFlap = calcChordLengthAtEta(etaKink + spanOuterFlap / span, parentWingVAMPzero, cpacsWing) * (1 - xsiSpar_interp(etaKink + spanOuterFlap / span)) - absSparOffset
        oldcalcArea = calcArea
        calcArea = spanOuterFlap * (cRootOuterFlap + cTipOuterFlap) / 2.

        if calcArea < oldcalcArea:
            log.warning('VAMPzero FLAP: Outer Flap Area can not be established! Continuing with outerArea = %s' % str(calcArea))
            newOuterFlapArea = calcArea
            break

        if spanOuterFlap / span + etaFus > maxEta:
            log.warning('VAMPzero FLAP: Outer Flap overlaps with the aileron! Continuing with outerArea = %s' % str(calcArea))
            newOuterFlapArea = calcArea
            break


    #===========================================================================
    # Determine the number of flaps
    # The aspect ratio of a flap should not be higher than 6.
    #===========================================================================
    nOuterFlaps = spanOuterFlap ** 2. / (newOuterFlapArea * 6.)
    log.debug('VAMPzero FLAP: Exporting %s Flaps outboard of the engine for an area of %s m2.' % (str(nOuterFlaps), str(newOuterFlapArea)))

    #===========================================================================
    # 1 Flap
    #===========================================================================
    if nOuterFlaps <= 1.:
        # the inner border eta is located at the kink
        innerEtaLE = etaFus + 0.05
        innerXsiLE = xsiSparRoot + sparOffset
        # the outer border eta is determined from the span of the outer flap
        outerEtaLE = etaFus + 0.05 + spanOuterFlap / span
        outerXsiLE = 1 - (cTipOuterFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))

        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))

    #===========================================================================
    # 2 Flaps
    #===========================================================================
    elif nOuterFlaps > 1. and nOuterFlaps <= 2.:
        # the inner border eta is located at the kink
        innerEtaLE = etaFus + 0.05
        innerXsiLE = xsiSparKink + sparOffset
        # the outer border eta is determined from the half span of the total outer flap
        outerEtaLE = etaFus + 0.05 + spanOuterFlap / (2*span)
        outerXsiLE = xsiSpar_interp(outerEtaLE) + absSparOffset / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='flap', innerX=innerX, outerX=outerX))

        # new inner is the old outer
        innerEtaLE = outerEtaLE
        innerXsiLE = outerXsiLE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaLE = etaFus + 0.05 + spanOuterFlap / span
        outerXsiLE = 1 - (cTipOuterFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))

        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap2', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))

    #===========================================================================
    # n Flaps
    #===========================================================================
    elif nOuterFlaps > 2. :
        n = int(ceil(nOuterFlaps))
        # First Flap
        # the inner border eta is located at the kink
        innerEtaLE = etaFus + 0.05
        innerXsiLE = xsiSparKink + sparOffset
        # the outer border eta is determined from the half span of the total outer flap
        outerEtaLE = etaFus + 0.05 + spanOuterFlap / (n*span)
        outerXsiLE = xsiSpar_interp(outerEtaLE) + absSparOffset / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)

        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='flap', innerX=innerX, outerX=outerX))

        for i in range(2, n):
            # nth Flap
            # new inner is the old outer
            innerEtaLE = outerEtaLE
            innerXsiLE = outerXsiLE
            # the outer border eta is determined from the full span of the total outer flap
            outerEtaLE = innerEtaLE + spanOuterFlap / n / span
            outerXsiLE = xsiSpar_interp(outerEtaLE) + absSparOffset / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)

            #Fowler Motion is restricted to 75% of the flap depth
            innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
            outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
            myFlaps.append(createFlap('outerFlap' + str(i), parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))


        # Last Flap
        # new inner is the old outer
        innerEtaLE = outerEtaLE
        innerXsiLE = outerXsiLE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaLE = etaFus + 0.05 + spanOuterFlap / span
        outerXsiLE = 1 - (cTipOuterFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))

        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap' + str(n), parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))


    #===============================================================================
    # Output to Spoiler
    # as the spoiler is relying on data of the flaps some basic information is written
    # back to the the VAMPzero components
    #===============================================================================
    parentWingVAMPzero.spoiler.outerEta = parameter(parent=parentWingVAMPzero.spoiler, value=outerEtaLE, unit='', status='calc', doc='The outermost eta coordinate of all flaps. This overlaps with the outer eta coordinate of the spoiler')
    spoilerChord = maxX
    parentWingVAMPzero.spoiler.chord = parameter(spoilerChord, 'm', 'calc', 'The absolute chord of the spoiler: 5% of the kink chord length + 50% of the innerFlap Chord length', parent=parentWingVAMPzero.spoiler)

    #===========================================================================
    # Output to CPACS
    #===========================================================================
    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_trailingEdgeDevices(trailingEdgeDevicesType())

    log.debug('VAMPzero SLAT: Exporting %s Flaps to CPACS.' % (str(len(myFlaps))))
    for flap in myFlaps:
        cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices().add_trailingEdgeDevice(flap)



def createFlapsAdvDoubleTrapezoid(parentWingCPACS, parentWingVAMPzero, myFlap):
    '''
    This is the main export method for the wings flaps
    
    @todo: it is possible that the inner flap overlaps the kink area
    '''
    cpacsPath = '/cpacs/vehicles/aircraft/model/wings/wing[' + parentWingVAMPzero.id + ']'
    cpacsWing = getObjfromXpath(parentWingCPACS, cpacsPath)
    cpacsComponentSegment = cpacsWing.get_componentSegments().get_componentSegment()[0]
    myFlaps = []
    
    #===========================================================================
    # Initialization, i.e. fetching values throughout the code
    #===========================================================================
    xsiSparRoot = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[3].get_xsi().valueOf_)
    xsiSparFuselage = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[4].get_xsi().valueOf_)
    xsiSparKink = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[5].get_xsi().valueOf_)
    xsiSparTip = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[6].get_xsi().valueOf_)

    etaSparRoot = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[3].get_eta().valueOf_)
    etaSparFuselage = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[4].get_eta().valueOf_)
    etaSparKink = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[5].get_eta().valueOf_)
    etaSparTip = eval(cpacsComponentSegment.get_structure().get_spars().get_sparPositions().get_sparPosition()[6].get_eta().valueOf_)

    xsiSpar_interp = scipy.interpolate.interp1d([etaSparRoot, etaSparFuselage, etaSparKink, etaSparTip], [xsiSparRoot, xsiSparFuselage, xsiSparKink, xsiSparTip])
    
    yFus = parentWingVAMPzero.yFuselage.getValue()
    span = parentWingVAMPzero.span.getValue() / 2.
    etaFus = yFus / span
    etaKink = parentWingVAMPzero.etaKink.getValue()
    cRoot = parentWingVAMPzero.cRoot.getValue()
    cKink = calcChordLengthAtEta(etaKink, parentWingVAMPzero, cpacsWing)
    phiLE = parentWingVAMPzero.phiLE.getValue()
    
    innerFlapArea = myFlap.refAreaInnerFlap.getValue()
    outerFlapArea = myFlap.refAreaOuterFlap.getValue()

    #===========================================================================
    # InnerFlap
    #===========================================================================
    #===========================================================================
    # Determine the number of flaps
    # The aspect ratio of a flap should not be higher than 9.
    #===========================================================================
    sparOffset = 0.08
    if phiLE > 0.:
        # if the wing is backward swept the chord of the inner flap equals the chord at kink behind the rear spar + sparOffset
        cInnerFlap = cKink * (1. - (xsiSparKink + sparOffset))
    elif phiLE < 0.:
        # if the wing is forward swept the chord of the inner flap is similar to the chord of the root section behind the spar + 20%
        cInnerFlap = cRoot * (1. - (xsiSparFuselage + 0.2))
    
    # maxX is the maximum extension of the flap
    maxX = cInnerFlap / 2.
    
    # The area of the innerFlap is determined by the chord and span 
    # The difference in the area will be substituted by the outerFlap Area
    spanInnerFlap = (etaKink - etaFus) * span
    newInnerFlapArea = cInnerFlap * spanInnerFlap
    deltaArea = innerFlapArea - newInnerFlapArea
    nInnerFlaps = spanInnerFlap ** 2. / (newInnerFlapArea * 9.)
    log.debug('VAMPzero FLAP: Exporting %s Flaps inside of the engine for an area of %s m2.' % (str(nInnerFlaps), str(innerFlapArea)))
        
    if nInnerFlaps < 1.:
        # the inner border eta is located at the intersection with the fuselage 
        innerEtaLE = etaFus
        # the inner border xsi is determined from the wing chord at the fuselage station (which equals CRoot)
        innerXsiLE = 1. - (cInnerFlap / cRoot)
        # the outer border eta is determined from the span of the inner flap
        outerEtaLE = etaKink
        # the outer xsi location is found from the avg chord and the chord length at that station
        outerXsiLE = 1. - (cInnerFlap / cKink)

        myFlaps.append(createFlap('innerFlap', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='innerFlap', innerX=maxX, outerX=maxX))
    
    elif nInnerFlaps > 1. and nInnerFlaps <= 2.:
        #=======================================================================
        # First Flap
        #=======================================================================
        # the inner border eta is located at the intersection with the fuselage 
        innerEtaLE = etaFus
        # the inner border xsi is determined from the wing chord at the fuselage station (which equals CRoot)
        innerXsiLE = 1. - (cInnerFlap / cRoot)
        # the outer border eta is determined from the span of the inner flap
        outerEtaLE = etaFus + (etaKink - etaFus) / 2.
        # the outer xsi location is found from the avg chord and the chord length at that station
        outerXsiLE = 1. - (cInnerFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))

        myFlaps.append(createFlap('innerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='innerFlap', innerX=maxX, outerX=maxX))
        
        #=======================================================================
        # Second Flap
        #=======================================================================
        # new inner is old outer
        innerEtaLE = outerEtaLE
        # new outer is kink
        outerEtaLE = etaKink
        # new inner is old outer
        innerXsiLE = outerXsiLE
        # new outer is kink
        outerXsiLE = 1. - (cInnerFlap / cKink)

        myFlaps.append(createFlap('innerFlap2', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='flap', innerX=maxX, outerX=maxX))

    
    #===========================================================================
    # OuterFlap
    #===========================================================================
    newOuterFlapArea = outerFlapArea + deltaArea
    cRootOuterFlap = cKink * (1. - (xsiSparKink + sparOffset))
    
    #===========================================================================
    # Determine the total flap span by iteration  
    #===========================================================================
    calcArea = 0.
    spanOuterFlap = 0.
    absSparOffset = sparOffset * cKink
    
    # Obtain the maxEtaValue. This is forwarded from the ailerons export routine.
    maxEta = myFlap.maxEta.getValue() - 0.02
    
    # the tip root length is a function of the span (as the xsi location of the spar changes)
    while abs(calcArea - newOuterFlapArea) > 0.1:
        spanOuterFlap += .01
        cTipOuterFlap = calcChordLengthAtEta(etaKink + spanOuterFlap / span, parentWingVAMPzero, cpacsWing) * (1 - xsiSpar_interp(etaKink + spanOuterFlap / span)) - absSparOffset
        oldcalcArea = calcArea
        calcArea = spanOuterFlap * (cRootOuterFlap + cTipOuterFlap) / 2.
        
        if calcArea < oldcalcArea:
            log.warning('VAMPzero FLAP: Outer Flap Area can not be established decreasing spar offset by 2% chord!')
            sparOffset = sparOffset - 0.02
            calcArea = 0.
            spanOuterFlap = 0.
            absSparOffset = sparOffset * cKink
            break
        
        if spanOuterFlap / span + etaKink > maxEta:
            log.warning('VAMPzero FLAP: Outer Flap overlaps with the aileron decreasing spar offset by 2% chord!')
            sparOffset = sparOffset - 0.02
            calcArea = 0.
            spanOuterFlap = 0.
            absSparOffset = sparOffset * cKink
            break
            

    while abs(calcArea - newOuterFlapArea) > 0.1:
        spanOuterFlap += .01
        cTipOuterFlap = calcChordLengthAtEta(etaKink + spanOuterFlap / span, parentWingVAMPzero, cpacsWing) * (1 - xsiSpar_interp(etaKink + spanOuterFlap / span)) - absSparOffset
        oldcalcArea = calcArea
        calcArea = spanOuterFlap * (cRootOuterFlap + cTipOuterFlap) / 2.
        
        if calcArea < oldcalcArea:
            log.warning('VAMPzero FLAP: Outer Flap Area can not be established! Continuing with outerArea = %s' % str(calcArea))
            newOuterFlapArea = calcArea
            break

        if spanOuterFlap / span + etaKink > maxEta:
            log.warning('VAMPzero FLAP: Outer Flap overlaps with the aileron! Continuing with outerArea = %s' % str(calcArea))
            newOuterFlapArea = calcArea
            break
        
   
    #===========================================================================
    # Determine the number of flaps
    # The aspect ratio of a flap should not be higher than 9. 
    #===========================================================================
    nOuterFlaps = spanOuterFlap ** 2. / (newOuterFlapArea * 9.)
    log.debug('VAMPzero FLAP: Exporting %s Flaps outboard of the engine for an area of %s m2.' % (str(nOuterFlaps), str(newOuterFlapArea)))
    
    #===========================================================================
    # 1 Flap
    #===========================================================================
    if nOuterFlaps <= 1.:
        # the inner border eta is located at the kink 
        innerEtaLE = etaKink
        innerXsiLE = xsiSparKink + sparOffset
        # the outer border eta is determined from the span of the outer flap
        outerEtaLE = etaKink + spanOuterFlap / span
        outerXsiLE = 1 - (cTipOuterFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))
        
        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))
    
    #===========================================================================
    # 2 Flaps
    #===========================================================================
    elif nOuterFlaps > 1. and nOuterFlaps <= 2.:
        # the inner border eta is located at the kink 
        innerEtaLE = etaKink
        innerXsiLE = xsiSparKink + sparOffset
        # the outer border eta is determined from the half span of the total outer flap
        outerEtaLE = etaKink + spanOuterFlap / (2. * span)
        outerXsiLE = xsiSpar_interp(outerEtaLE) + absSparOffset / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='flap', innerX=innerX, outerX=outerX))
        
        # new inner is the old outer 
        innerEtaLE = outerEtaLE
        innerXsiLE = outerXsiLE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaLE = etaKink + spanOuterFlap / span
        outerXsiLE = 1 - (cTipOuterFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))

        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap2', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))
    
    #===========================================================================
    # n Flaps
    #===========================================================================
    elif nOuterFlaps > 2. :
        n = int(ceil(nOuterFlaps))
        # First Flap
        # the inner border eta is located at the kink 
        innerEtaLE = etaKink
        innerXsiLE = xsiSparKink + sparOffset
        # the outer border eta is determined from the half span of the total outer flap
        outerEtaLE = etaKink + spanOuterFlap / n / span
        outerXsiLE = xsiSpar_interp(outerEtaLE) + absSparOffset / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
        
        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap1', parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, type='flap', innerX=innerX, outerX=outerX))
        
        for i in range(2, n):
            # nth Flap
            # new inner is the old outer 
            innerEtaLE = outerEtaLE
            innerXsiLE = outerXsiLE
            # the outer border eta is determined from the full span of the total outer flap
            outerEtaLE = innerEtaLE + spanOuterFlap / n / span
            outerXsiLE = xsiSpar_interp(outerEtaLE) + absSparOffset / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing)
            
            #Fowler Motion is restricted to 75% of the flap depth
            innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
            outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
            myFlaps.append(createFlap('outerFlap' + str(i), parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))
        
        
        # Last Flap
        # new inner is the old outer 
        innerEtaLE = outerEtaLE
        innerXsiLE = outerXsiLE
        # the outer border eta is determined from the full span of the total outer flap
        outerEtaLE = etaKink + spanOuterFlap / span
        outerXsiLE = 1 - (cTipOuterFlap / calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing))
        
        #Fowler Motion is restricted to 75% of the flap depth
        innerX = (1. - innerXsiLE) * calcChordLengthAtEta(innerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        outerX = (1. - outerXsiLE) * calcChordLengthAtEta(outerEtaLE, parentWingVAMPzero, cpacsWing) * 0.5
        myFlaps.append(createFlap('outerFlap' + str(n), parentWingVAMPzero.id, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=True, type='flap', innerX=innerX, outerX=outerX))


    #===============================================================================
    # Output to Spoiler
    # as the spoiler is relying on data of the flaps some basic information is written 
    # back to the the VAMPzero components  
    #===============================================================================
    parentWingVAMPzero.spoiler.outerEta = parameter(outerEtaLE, '', 'calc', 'The outermost eta coordinate of all flaps. This overlaps with the outer eta coordinate of the spoiler', parent=parentWingVAMPzero.spoiler)
    spoilerChord = 0.05 * cKink + 0.5 * cInnerFlap
    parentWingVAMPzero.spoiler.chord = parameter(spoilerChord, 'm', 'calc', 'The absolute chord of the spoiler: 5% of the kink chord length + 50% of the innerFlap Chord length', parent=parentWingVAMPzero.spoiler)
    
    #===========================================================================
    # Output to CPACS
    #===========================================================================
    if type(cpacsComponentSegment.get_controlSurfaces()) == NoneType:
        cpacsComponentSegment.set_controlSurfaces(controlSurfacesType())
    if type(cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices()) == NoneType:
        cpacsComponentSegment.get_controlSurfaces().set_trailingEdgeDevices(trailingEdgeDevicesType())
    
    log.debug('VAMPzero SLAT: Exporting %s Flaps to CPACS.' % (str(len(myFlaps))))
    for flap in myFlaps:
        cpacsComponentSegment.get_controlSurfaces().get_trailingEdgeDevices().add_trailingEdgeDevice(flap)
    
    
def createFlap(name, parentUID, innerEtaLE, innerXsiLE, outerEtaLE, outerXsiLE, maxX, appendInnerCruiseRoller=False, type='flap', innerX=0., outerX=0.):
    log.debug('VAMPzero FLAP: Creating Flap: %s' % (str(name)))
    log.debug('VAMPzero FLAP: innerEtaLE: %s' % str(innerEtaLE))
    log.debug('VAMPzero FLAP: outerEtaLE: %s' % str(outerEtaLE))
    log.debug('VAMPzero FLAP: innerXsiLE: %s' % str(innerXsiLE))
    log.debug('VAMPzero FLAP: outerXsiLE: %s' % str(outerXsiLE))
    
    myName = stringBaseType(None, None, None, name)
    myDescription = stringBaseType(None, None, None, 'innerFlap from VAMPzero')
    myParentUID = stringUIDBaseType(None, None, 'True', None, parentUID)

    myleadingEdgeShape = leadingEdgeShapeType(relHeightLE=doubleBaseType(valueOf_=str(0.2)), xsiUpperSkin=doubleBaseType(valueOf_=str(0.5)), xsiLowerSkin=doubleBaseType(valueOf_=str(0.95)))
    innerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(innerEtaLE)), etaTE=doubleBaseType(valueOf_=str(innerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(innerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    outerBorder = controlSurfaceBorderTrailingEdgeType(etaLE=doubleBaseType(valueOf_=str(outerEtaLE)), etaTE=doubleBaseType(valueOf_=str(outerEtaLE)), xsiLE=doubleBaseType(valueOf_=str(outerXsiLE)), leadingEdgeShape=myleadingEdgeShape)
    
    myOuterShape = controlSurfaceOuterShapeTrailingEdgeType(innerBorder=innerBorder, outerBorder=outerBorder)
    myStructure = wingComponentSegmentStructureType()
    myFlap = trailingEdgeDeviceType(uID=name + 'UID', name=myName, description=myDescription, parentUID=myParentUID, outerShape=myOuterShape, structure=myStructure)
    createFlapStructure(myFlap, maxX, innerXsiLE, outerXsiLE, appendInnerCruiseRoller, type=type, innerX=innerX, outerX=outerX)
    return myFlap

def createFlapStructure(myFlap, maxX=0.4, innerHingeXsi=0.7, outerHingeXsi=0.7, appendInnerCruiseRoller=False, type='flap', innerX=0., outerX=0.):
    myUID = myFlap.get_uID()

    # Structure    
    createShell(myFlap, myUID, type, thickness=0.001)
    createSpars(myFlap, myUID, type)
    createRibs(myFlap, myUID, type, thickness=0.001, nRibs=20)

    # Moveables
    createTracks(myFlap, type, myUID)
    createPath(myFlap, type, myUID, innerX, outerX, innerHingeXsi, outerHingeXsi)
    if appendInnerCruiseRoller:
        createCruiseRollers(myFlap, 'outerFlap', myUID + '_CR1')

