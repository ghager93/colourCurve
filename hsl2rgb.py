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
    
    return out


def _hex_segment(h_dash, seg):
    return (h_dash >= seg) & (h_dash < seg + 1)


def _rgb_normalise(RGB, m):
    RGB_reshaped = np.moveaxis(RGB, -1, 0)
    out = np.moveaxis(RGB_reshaped + m, 0, -1)
    return out


def hsl2rgb(h, s, l):
    h_dash = _h_dash_func(h)
    c = _c_func(s, l)
    x = _x_func(c, h_dash)
    return _rgb_normalise(_rgb_raw(h_dash, c, x), _m_func(l, c))


def rgb_square_grid(resolution, l=0.5, h_min=0, h_max=360, s_min=0, s_max=1, l_min=0, l_max=1):
    
    h = np.linspace(h_min, h_max, resolution[0], endpoint=False)
    s = np.linspace(s_min, s_max, resolution[1], endpoint=False)
    
    if len(resolution) == 2:
        h_1, s_1 = np.meshgrid(h, s)
        l_1 = l
    elif len(resolution) == 3:
        l = np.linspace(l_min, l_max, resolution[2], endpoint=False)
        h_1, s_1, l_1 = np.meshgrid(h, s, l)
    else:
        print(len(resolution))
        return -1
        
    return hsl2rgb(h_1, s_1, l_1)
