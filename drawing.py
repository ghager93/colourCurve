import numpy as np

from scipy.special import binom
from wrapt import function_wrapper


class ParameterisedCurve:
    def t_function(self, t):
        pass

    def get_equidistant_points(self, n_points):
        return [self.t_function(t) for t in np.linspace(0, 1, n_points)]


class ParameterisedLine(ParameterisedCurve):
    def __init__(self, p1, p2):
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)

    def t_function(self, t):
        return t*self.p2 + (1-t)*self.p1


class ParameterisedCircle(ParameterisedCurve):
    def __init__(self, radius, centre):
        self.radius = radius
        self.centre = np.array(centre)

    def t_function(self, t):
        return self.radius*np.cos(2*np.pi*t) + self.centre[0], self.radius*np.sin(2*np.pi*t) + self.centre[1]


class ParameterisedEllipse(ParameterisedCurve):
    def __init__(self, radius_x, radius_y, centre):
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.centre = np.array(centre)

    def t_function(self, t):
        return self.radius_x*np.cos(2*np.pi*t) + self.centre[0], self.radius_y*np.sin(2*np.pi*t) + self.centre[1]


class ParameterisedRotatedEllipse(ParameterisedCurve):
    def __init__(self, radius_x, radius_y, centre, rotation):
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.centre = np.array(centre)
        self.rotation = rotation

    def t_function(self, t):
        return self._x_t(t), self._y_t(t)

    def _x_t(self, t):
        return self.radius_x*np.cos(2*np.pi*t)*np.cos(self.rotation) \
               - self.radius_y*np.sin(2*np.pi*t)*np.sin(self.rotation) \
               + self.centre[0]

    def _y_t(self, t):
        return self.radius_x*np.cos(2*np.pi*t)*np.sin(self.rotation) \
               + self.radius_y*np.sin(2*np.pi*t)*np.cos(self.rotation) \
               + self.centre[1]


class ParameterisedBezier(ParameterisedCurve):
    def __init__(self, points):
        self.points = [np.array(p) for p in points]
        self.n = len(points)
        self._binomial_coeffs = self._get_binomial_coeffs()

    def _get_binomial_coeffs(self):
        return [binom(self.n-1, i) for i in range(self.n)]

    def t_function(self, t):
        p_t = 0

        for i in range(self.n):
            coeff = self._binomial_coeffs[i] * (1-t)**(self.n-i-1) * t**i
            p_t += coeff * self.points[i]

        return p_t


class ParameterisedRationalBezier(ParameterisedBezier):
    def __init__(self, points, weights):
        super().__init__(points)
        self.weights = weights

    def t_function(self, t):
        p_t, denom = 0, 0

        for i in range(self.n):
            weighted_coeff = self.weights[i] * self._binomial_coeffs[i] * (1-t)**(self.n-i-1) * t**i

            p_t += weighted_coeff * self.points[i]
            denom += weighted_coeff

        return p_t / denom


class ParameterisedPiecewiseLine(ParameterisedCurve):
    def __init__(self, points):
        self.points = [np.array(p) for p in points]
        self.n = len(points)
        # self.total_length = self._get_total_length()
        self.cum_lengths = self._get_cum_lengths()

    def _get_total_length(self):
        return sum([self._dist(self.points[i+1], self.points[i]) for i in range(self.n-1)])

    @staticmethod
    def _dist(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def _get_cum_lengths(self):
        lengths = [self._dist(self.points[i+1], self.points[i]) for i in range(self.n-1)]
        total_length = sum(lengths)

        return np.concatenate([[0], np.cumsum(lengths) / total_length])

    def t_function(self, t):
        i = 0
        while t > self.cum_lengths[i]:
            i += 1

        t_i = (t - self.cum_lengths[i-1]) / (self.cum_lengths[i] - self.cum_lengths[i-1])

        return t_i * self.points[i] + (1 - t_i) * self.points[i-1]
