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
from VAMPzero.Handler.Parameter import parameter


class active(parameter):
    '''
    This parameter determines whether the strut is active or not, i.e., whether the configuration is a strut braced wing or not.active

    Default: 0

    :Unit: [ ]
    '''

    def __init__(self, value=0., unit='', parent='', cpacsPath=''):
        super(active, self).__init__(value=value, unit=unit, doc=self.__doc__, status='fix', parent=parent,
                                          cpacsPath=cpacsPath)

    def calc(self):
        '''
        If the value of the parameter is false and fixed then all other strut values are set to zero
        '''
        if self.getStatus() != 'fix':
            return self.setValueCalc(0.)

        if self.getStatus() == 'fix' and not self.getValue():
            for para in sorted(self.parent.__dict__, key=str.lower):
                para = getattr(self.parent, para)

                if issubclass(para.__class__, parameter):
                    para.setValueFix(0.0)




###################################################################################################
#EOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFEOFE#
###################################################################################################