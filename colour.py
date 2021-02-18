import numpy as np

import convert_hsl2rgb
import convert_rgb2hsl


def hsl2rgb(hue, saturation, lightness):
    return convert_hsl2rgb.hsl2rgb(hue, saturation, lightness)


def rgb2hsl(red, blue, green):
    return convert_rgb2hsl.rgb2hsl(red, blue, green)


def hsl_square_grid(resolution=(256, 256), l=0.5, h_min=0, h_max=360, s_min=0, s_max=1, l_min=0, l_max=1):
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

    return h_1, s_1, l_1


def rgb_square_grid(resolution=(256, 256), l=0.5, h_min=0, h_max=360, s_min=0, s_max=1, l_min=0, l_max=1):
    return hsl2rgb(*hsl_square_grid(resolution, l, h_min, h_max, s_min, s_max, l_min, l_max))


def image2hsl(image):
    return rgb2hsl(image.transpose(2, 0, 1)).transpose(1, 2, 0)

