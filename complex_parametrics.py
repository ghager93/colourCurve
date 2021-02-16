import numpy as np
import cmath

from drawing import ParameterisedCurve


class ParameterisedComplexLine(ParameterisedCurve):
    def __init__(self, cp1: complex, cp2: complex):
        self.cp1 = cp1
        self.cp2 = cp2

    def t_function(self, t):
        return (1 - t) * self.cp1 + t * self.cp2


class ParameterisedComplexCurve1(ParameterisedCurve):
    def __init__(self, cp1: complex, cp2: complex):
        self.cp1 = cp1
        self.cp2 = cp2

    def t_function(self, t):
        return cmath.rect(self._r(t), self._phi(t))

    def _r(self, t):
        return (1 - t) * abs(self.cp1) + t * abs(self.cp2)

    def _phi(self, t):
        return (1 - t) * cmath.phase(self.cp1) + t * cmath.phase(self.cp2)

class ParameterisedComplexCurve2(ParameterisedCurve):
    def __init__(self, cp1: complex, cp2: complex):
        self.cp1 = cp1
        self.cp2 = cp2

    def t_function(self, t):
        return cmath.rect((1 - t) * abs(self.cp1), (1 - t) * cmath.phase(self.cp1)) \
               + cmath.rect(t * abs(self.cp2), t * cmath.phase(self.cp2))
