import numpy as np


def _h_dash_func(h): return (h % 360) / 60


def _c_func(s, l): return s * (1 - np.abs(2 * l - 1))


def _x_func(c, h_dash): return c * (1 - np.abs(h_dash % 2 - 1))


def _m_func(l, c): return l - c / 2


def _rgb_raw(h_dash, c, x):
    h_dash = np.array(h_dash)
    c = np.array(c)
    x = np.array(x)
    
    out = np.zeros((*h_dash.shape, 3))
    
    h_seg = _hex_segment(h_dash, 0)
    out[h_seg, 0] = c[h_seg]
    out[h_seg, 1] = x[h_seg]
    out[h_seg, 2] = 0.
    
    h_seg = _hex_segment(h_dash, 1)
    out[h_seg, 0] = x[h_seg]
    out[h_seg, 1] = c[h_seg]
    out[h_seg, 2] = 0.
    
    h_seg = _hex_segment(h_dash, 2)
    out[h_seg, 0] = 0.
    out[h_seg, 1] = c[h_seg]
    out[h_seg, 2] = x[h_seg]
    
    h_seg = _hex_segment(h_dash, 3)
    out[h_seg, 0] = 0.
    out[h_seg, 1] = x[h_seg]
    out[h_seg, 2] = c[h_seg]
    
    h_seg = _hex_segment(h_dash, 4)
    out[h_seg, 0] = x[h_seg]
    out[h_seg, 1] = 0.
    out[h_seg, 2] = c[h_seg]
    
    h_seg = _hex_segment(h_dash, 5)
    out[h_seg, 0] = c[h_seg]
    out[h_seg, 1] = 0.
    out[h_seg, 2] = x[h_seg]
    
    return out.transpose(2, 0, 1)


def _hex_segment(h_dash, seg):
    return (h_dash >= seg) & (h_dash < seg + 1)


def _rgb_normalise(rgb, m):
    return rgb + m


def hsl2rgb(h, s, l):
    h_dash = _h_dash_func(_normalise_h(h))
    c = _c_func(s, l)
    x = _x_func(c, h_dash)

    return _rgb_normalise(_rgb_raw(h_dash, c, x), _m_func(l, c))


def _normalise_h(h):
    if np.max(h) <= 1:
        h *= 360

    return h

