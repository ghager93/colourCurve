import numpy as np


def _fc_max(r, g, b):
    return np.maximum(r, np.maximum(g, b))


def _fc_min(r, g, b):
    return np.minimum(r, np.minimum(g, b))


def _fdelta(c_max, c_min):
    return c_max - c_min


def _fh(r, g, b, delta, c_max):
    delta_no_zeros = np.where(delta == 0, 1, delta)

    def cmax_is_r():
        return (((g - b) / delta_no_zeros) % 6) / 6
    def cmax_is_g():
        return (((b - r) / delta_no_zeros) + 2) / 6
    def cmax_is_b():
        return (((r - g) / delta_no_zeros) + 4) / 6

    out = np.zeros(delta.shape)
    out = np.where((c_max == r) & (delta != 0), cmax_is_r(), out)
    out = np.where((c_max == g) & (delta != 0), cmax_is_g(), out)
    out = np.where((c_max == b) & (delta != 0), cmax_is_b(), out)
    
    return out


def _fs(delta, vl):
    vl_no_ones_and_zeroes = np.where((vl == 0) | (vl == 1), 0.5, vl)
    return np.where((vl != 0) & (vl != 1), delta / (1 - np.abs(2 * vl_no_ones_and_zeroes - 1)), 0)


def _fl(c_max, c_min):
    return (c_max + c_min) / 2


def rgb2hsl(r, g, b):
    if np.max([r, g, b]) > 1:
        r = r / 255
        g = g / 255
        b = b / 255
        
    c_max = _fc_max(r, g, b)
    c_min = _fc_min(r, g, b)
    delta = _fdelta(c_max, c_min)
    
    h = _fh(r, g, b, delta, c_max)
    vl = _fl(c_max, c_min)
    s = _fs(delta, vl)
    
    return np.array([h, s, vl])
