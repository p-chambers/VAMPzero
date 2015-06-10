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

from logging import Logger
import logging
import os
import sys



logFile             = './ReturnDirectory/VAMPzero.log'


class zeroLogger(Logger):
    '''
    Instances of ZeroLogger can be used for Logging in VAMPzero. zeroLogger inherits pythons standard
    logging functionalities
    '''

    _FileHandle     = None
    _StreamHandle   = None

    def setFileHandler(self):
        '''
        Setting up the File Handler and its format. The FileHandler will work on
        debug level.
        '''
        if zeroLogger._FileHandle == None:
            FileHandler              = logging.FileHandler(logFile)
            Fileformatter            = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            FileHandler.setLevel(logging.DEBUG)
            FileHandler.setFormatter(Fileformatter)
            zeroLogger._FileHandle = FileHandler


    def setStreamHandler(self):
        '''
        Setting up the Stream Handler and its format. The StreamHandler is set to Info level.
        '''
        if zeroLogger._StreamHandle == None:
            StreamHandler             = logging.StreamHandler(sys.stdout)
            Streamformatter           = logging.Formatter('%(levelname)-8s %(message)s')
            StreamHandler.setFormatter(Streamformatter)
            StreamHandler.setLevel(logging.INFO)
            zeroLogger._StreamHandle  = StreamHandler


    def __init__(self,name):
        '''
        new constructor already setting up the different handlers and formatters
        '''
        Logger.__init__(self,name)

        #Flag whether a file log should be created
        fileLog = True

        #Checking whether there is a folder for logging
        if not os.path.isdir(os.path.dirname(logFile)):
            fileLog = False

        #If our log file exists we delete it to have a new log file for every run
        if os.path.isfile(logFile) and fileLog:
            try:
                os.remove(logFile)
            except:
                pass

        if fileLog:
            self.setFileHandler()
            self.addHandler(zeroLogger._FileHandle)

        self.setStreamHandler()
        self.addHandler(zeroLogger._StreamHandle)


    def close(self):
        '''
        Kills all handlers that can be found within the instance
        '''
        for handler in self.handlers:
            handler.close()
    
    def write(self,data):
        self.info(str(data))