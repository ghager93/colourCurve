import numpy as np

from PIL import Image
from sklearn.cluster import KMeans, MiniBatchKMeans

from colour import *


def classify(points, n_clusters: int):
    return _by_k_means(points, n_clusters)


def _by_mini_batch_k_means(points, n_clusters: int):
    k_means = MiniBatchKMeans(n_clusters=n_clusters).fit(points)
    return k_means.cluster_centers_, k_means.labels_


def _by_k_means(points, n_clusters: int):
    k_means = KMeans(n_clusters=n_clusters).fit(points)
    return k_means.cluster_centers_, k_means.labels_


def sample_image(image, n_samples):
    sampling_ratio = n_samples / (image.shape[0] * image.shape[1])
    sampling_mask = np.random.choice([False, True],
                                    (image.shape[0], image.shape[1]),
                                    p=[1 - sampling_ratio, sampling_ratio])
    return image[sampling_mask]


def image_centroids(image, n_centroids):
    MAX_SAMPLE = 10000

    if image.shape[0] * image.shape[1] > MAX_SAMPLE:
        im_points = sample_image(image, MAX_SAMPLE)
    else:
        im_points = np.reshape(np.copy(image), (-1, 3))

    return KMeans(n_centroids).fit(im_points).cluster_centers_
