#@todo: reset all properties for the svn, check for headers
#@todo: update all sources 
#@todo: check for fixed parameters if self is fixed
version = "0.6.4"

import sys
import argparse
import VAMPzero.Lib.CPACS.general as generalLib
import VAMPzero.Component.Main.aircraft as aircraftLib
import VAMPzero.Lib.Matlab.importMatlab as importMatlabLib
import VAMPzero.Lib.GUI.gui as guiLib
import VAMPzero.Lib.TIXI.tixi as tixiLib
import VAMPzero.Lib.CPACS.Export.export as exportLib
import VAMPzero.Lib.Matplotlib.plotAircraft as plotAircraftLib
import VAMPzero.Lib.CPACS.cpacs as cpacsLib
from VAMPzero.Handler.Exceptions import NotConvergingError
import shutil

class Vampzero(object):
    '''
    This class implements a convenience interface to setup a VAMPzero run.
    '''

    def __init__(self, cpacsIn=None, cpacsOut=None, resultFile=None, resultOnErrorFile=None):
        '''
        Initialize VAMPzero with standard properties.
        '''
        if cpacsIn == None:
            cpacsIn = "./ToolInput/toolInput.xml"
        self.cpacsIn = cpacsIn
        
        if cpacsOut == None:
            cpacsOut = "./ToolOutput/toolOutput.xml"
        self.cpacsOut    = cpacsOut
        
        if resultFile == None:
            resultFile = "./ReturnDirectory/VAMPzero.m"
        self.resultFile  = resultFile
        
        if resultOnErrorFile == None:
            resultOnErrorFile = "./ReturnDirectory/ResultOnError.m"
        self.resultOnErrorFile = resultOnErrorFile
        
        self.args = None
        self.config = {}
        self.aircraft = aircraftLib.aircraft()
        self.initParser()
    
    def readConfig(self):
        '''
        Read VAMPzeros configuration parameters. Command line arguments overwrite the configurations in the toolspecific part. 
        '''
        TIXIHandle      = tixiLib.openTIXI(self.cpacsIn)
        if self.args.d != None:
            self.config['deviationAmplitude'] = float(self.args.d)
        else:
            devFactor = 0.0
            devFactorStr = tixiLib.getText(TIXIHandle,'/cpacs/toolspecific/vampZero/toolSettings/deviationAmplitude')
            if devFactorStr != None:
                devFactor = float(devFactorStr)
            self.config['deviationAmplitude'] = devFactor
        # read configuration for extended output
        self.config['extendedOutput'] = True
        extendedOutput = tixiLib.getText(TIXIHandle,'/cpacs/toolspecific/vampZero/toolSettings/extendedOutput')
        if extendedOutput in ('False', 'false', '0.0', '0.', '0'):
            self.config['extendedOutput'] = False
        # read sensitivity configuration
        self.config['calcSensitivities'] = False
        calcSensitivities = tixiLib.getText(TIXIHandle,'/cpacs/toolspecific/vampZero/toolSettings/calcSensitivities')
        if calcSensitivities in ('True', 'true', '1.0', '1.', '1'):
            self.config['calcSensitivities'] = True
        # read not converging behavior
        self.config['notConvergingAction'] = 'exit'
        not_converging_action = tixiLib.getText(TIXIHandle,'/cpacs/toolspecific/vampZero/toolSettings/notConvergingAction')
        if not_converging_action in ('exit', 'copyInput', 'errorXML'):
            self.config['notConvergingAction'] = not_converging_action
        tixiLib.closeXML(TIXIHandle)
    
    def initParser(self):
        '''
        Initializes the argument parser to process command line arguments.
        '''
        #usage = "usage: %prog [options] arg1 arg2\n\ttype '%prog --help' for help"
        self.parser = argparse.ArgumentParser(prog='VAMPzero')
        self.parser.add_argument('-m', action='store_true', help='import Matlab')
        self.parser.add_argument('-d', default=None, help='calculate deviation')
#        self.parser.add_argument('--no_plots', action='store_false', help='deactivates plotting')
    
    def run(self, argv=None):
        '''
        Runs VAMPzero.
        '''
        if argv is None:
            argv = sys.argv
        try:
            generalLib.printHeader()
            print argv
            self.args = self.parser.parse_args()
            self.readConfig()
            ###################################################################################################
            ##VAMPzero Initialize
            ###################################################################################################
            self.aircraft.engine.sfcCR.calc = self.aircraft.engine.sfcCR.calcOverallEff
            self.setFixed()
            
            ###################################################################################################
            ##VAMPzero Imports
            ###################################################################################################
            if self.args.m:
                importMatlabLib.importMatlab(self.aircraft)
            else:
                guiLib.importGUI(self.aircraft, self.cpacsIn)
            
            tixiHandle  = tixiLib.openTIXI(self.cpacsIn)
            hasModel    = tixiLib.checkElement(tixiHandle,'/cpacs/vehicles/aircraft/model')
            if hasModel:
                self.aircraft.cpacsImport(self.cpacsIn)

            self.aircraft.atmosphere.hCR.setValueFix(self.aircraft.altCR.getValue())
            self.aircraft.atmosphere.MaCR.setValueFix(self.aircraft.machCR.getValue())
            
            self.calc()
            self.finish()
            self.setUIDs()
            
            self.exportToolspecific() # needs to be called after the last use of cpacsLib (otherwise all nodes not in the schema will be removed)
            generalLib.printFooter()
            
            return 0
            
        except (argparse.ArgumentError), err:
            print >>sys.stderr, err
            self.parser.print_help()
            return 2
        
        except (NotConvergingError), err:
            # write output to help with debugging
            exportLib.resultExport(self.aircraft, self.resultOnErrorFile, componentWise=True)
            
            if self.config['notConvergingAction'] in ('copyInput'):
                shutil.copyfile(self.cpacsIn, self.cpacsOut)
                TIXIHandle = tixiLib.openTIXI(self.cpacsOut)
                tixiLib.addText(TIXIHandle, '/cpacs/toolspecific/vampZero/toolSettings/exitCondition', 'NOT CONVERGED')
                tixiLib.saveXML(self.cpacsOut,TIXIHandle)
                tixiLib.closeXML(TIXIHandle)
            elif self.config['notConvergingAction'] in ('errorXML'):
                with open(self.cpacsOut, 'w') as outfile:
                    outfile.write('<cpacs><exitCondition>NOT CONVERGING</exitCondition></cpacs>')
            elif self.config['notConvergingAction'] in ('tryExportLastState'):
                self.finish()
                self.setUIDs()
                self.exportToolspecific()
            sys.exit()#@note: enter exit code here
        
    
    def setFixed(self):
        '''
        Sets fixed values
        This method can be monkey patched if needed.
        '''
        self.aircraft.htp.airfoilr.tc.setValueFix(0.1)
        self.aircraft.htp.airfoilt.tc.setValueFix(0.1)
        self.aircraft.vtp.airfoilr.tc.setValueFix(0.1)
        self.aircraft.vtp.airfoilt.tc.setValueFix(0.1)
    
    def calc(self):
        ###################################################################################################
        ##VAMPzero Calculate
        ###################################################################################################
        self.aircraft.inputs()
        self.aircraft.calcAuto(deviationAmplitude=self.config['deviationAmplitude'] ,debug =False)
        self.aircraft.inits()

    def finish(self):
        ###################################################################################################
        ##VAMPzero Finish
        ###################################################################################################
        exportLib.cpacsExport(self.aircraft, self.cpacsOut)
        exportLib.resultExport(self.aircraft, self.resultFile, componentWise=True)
        
        self.aircraft.check()
        
        self.aircraft.report()
        
        # uncomment following line to create output mapping
        #outMapping(myAircraft)
        if self.config['extendedOutput']:
            self.aircraft.freemindExport(withValues = True)
            plotAircraftLib.plotAircraft(self.aircraft)
        
        if self.config['calcSensitivities']:
            self.aircraft.sensitivity()

    def setUIDs(self):
        ###################################################################################################
        ##Set UIDS
        ###################################################################################################
        CPACSObj        = cpacsLib.parse(self.cpacsOut)
        #UID for aircraft model
        cpacsPath       = '/cpacs/vehicles/aircraft/model'
        myCPACSAircraft = exportLib.getObjfromXpath(CPACSObj,cpacsPath)
        myCPACSAircraft.set_uID(self.aircraft.modelUID.getValue())
        
        #UID for engine
        cpacsPath       = '/cpacs/vehicles/aircraft/model/engines/engine'
        myCPACSEngine   = exportLib.getObjfromXpath(CPACSObj,cpacsPath)
        myCPACSEngine.set_uID(self.aircraft.engine.UID.getValue())
        
        #save and close
        outfile = open(self.cpacsOut,'w')
        CPACSObj.export(outfile,0)
        outfile.close()
    
    def exportToolspecific(self):
        '''
        Exports VAMPzeros own toolspecific part.
        This includes results for parameters which where marked for toolspecific export.
        '''
        return exportLib.resultToolspecExport(self.aircraft, self.cpacsOut)

