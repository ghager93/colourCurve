import numpy as np

from PIL import Image
from sklearn.cluster import KMeans, MiniBatchKMeans

from colour import *


def classify(points, n_clusters=int):
    return _by_mini_batch_k_means(points, n_clusters)


def _by_mini_batch_k_means(points, n_clusters: int):
    k_means = MiniBatchKMeans(n_clusters=n_clusters).fit(points)
    return k_means.cluster_centers_, k_means.labels_


def _by_k_means(points, n_clusters: int):
    k_means = KMeans(n_clusters=n_clusters).fit(points)
    return k_means.cluster_centers_, k_means.labels_