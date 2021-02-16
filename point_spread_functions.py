import numpy as np

def gaussian_3d_func(t, x0):
    t = np.atleast_1d(t)[:, None, None]
    x0 = np.atleast_1d(x0)[:, None, None]

    return lambda x: np.exp(-np.sum((x - x0)**2 / (2 * t**2), axis=0))
