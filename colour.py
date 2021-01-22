import numpy as np

import convert_hsl2rgb
import convert_rgb2hsl


def hsl2rgb(hue, saturation, lightness):
    return convert_hsl2rgb.hsl2rgb(hue, saturation, lightness)


def rgb2hsl(red, blue, green):
    return convert_rgb2hsl.rgb2hsl(red, blue, green)


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

