import numpy as np

from colour import rgb2hsl
from classify import image_centroids
from vector_mapping import VectorMap


def image2hsl(image):
    return rgb2hsl(*image.transpose(2, 0, 1)).transpose(1, 2, 0)


def image2hs_sample_map(image, samples):
    return hs_sample_map(image, samples)(image)


def hs_sample_map(image, samples):
    samples = np.atleast_2d(samples)

    im_hsl = image2hsl(image)
    hs_centroids = _hs_centroids(im_hsl, samples.shape[0])
    mapping_func = VectorMap(*hs_centroids.transpose(), *samples.transpose()).mapping_func()

    def hs_sample_map_func(x):
        hs = np.delete(x.transpose(2, 0, 1), 2, 0)
        return np.r_[mapping_func(hs), [x[:, :, 2]]]

    return hs_sample_map_func


def _hs_centroids(image, n_centroids):
    return np.delete(image_centroids(image, n_centroids), 2, 1)


def _hl_centroids(image, n_centroids):
    return np.delete(image_centroids(image, n_centroids), 1, 1)
