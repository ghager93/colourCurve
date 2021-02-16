import numpy as np
from PIL import Image

from colour import rgb_square_grid


def create_image(path='lib/images/rgb_square.png', resolution=(256, 256),
                 l=0.5, h_min=0, h_max=360, s_min=0, s_max=1, l_min=0, l_max=1):
    grid = rgb_square_grid(resolution, l, h_min, h_max, s_min, s_max, l_min, l_max)
    im = Image.fromarray((grid * 255.0).astype(np.uint8), 'RGB')
    im.save(path)


