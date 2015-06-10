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


class zeroComplex(complex):
    '''
    For using complexStep mechanisms this was implemented
    
    zeroComplex is used for two reasons: 
    
    1) in python complex can not be used for rich comparisons
       Therefore zeroComplex inherits complex and extends it by defining
       comparison operations that enable the comparison of the real 
       part
    
    2) As all remaining operations in python still return complex as 
       standard type, zeroComplex must force any object in interaction with
       itself to return zeroComplex.
       Therefore coerce and all math operators (still calling the super math operator) 
       convert and return zeroComplex objects
        
    '''

    def __coerce__(self, other):
        return self, zeroComplex(other)

    #===============================================================================
    # Math Operators
    #===============================================================================

    def __div__(self, other):
        if not isinstance(other, zeroComplex):
            other = zeroComplex(other)
        if other != zeroComplex(0.):
            result = super(zeroComplex, self).__div__(other)
            return zeroComplex(result)

    def __pow__(self, other):
        if not isinstance(other, zeroComplex):
            other = zeroComplex(other)

        result = super(zeroComplex, self).__pow__(other)
        return zeroComplex(result)

    def __add__(self, other):
        if not isinstance(other, zeroComplex):
            other = zeroComplex(other)

        result = super(zeroComplex, self).__add__(other)
        return zeroComplex(result)

    def __sub__(self, other):
        if not isinstance(other, zeroComplex):
            other = zeroComplex(other)

        result = super(zeroComplex, self).__sub__(other)
        return zeroComplex(result)


    def __mul__(self, other):
        if not isinstance(other, zeroComplex):
            other = zeroComplex(other)

        result = super(zeroComplex, self).__mul__(other)
        return zeroComplex(result)

    #===============================================================================
    # Conversions
    #===============================================================================

    def __int__(self):
        return int(self.real)

    #===============================================================================
    # Rich Comparison Operators
    #===============================================================================

    def __eq__(self, other):
        if self.real == other:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.real >= other:
            return True
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, complex):
            other = zeroComplex(other)
        if self.real > other:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.real < other:
            return True
        else:
            return False

    def __le__(self, other):
        if self.real <= other:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.real != other:
            return True
        else:
            return False