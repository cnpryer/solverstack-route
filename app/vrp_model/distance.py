import logging
from typing import List, Tuple

import numpy as np
from haversine import haversine_vector, Unit


def create_vectorized_haversine_li(
    origin: Tuple[float],
    dest_lons: List[float],
    dest_lats: List[float],
    unit: str = "mi",
):
    origin_lat = [origin[0]] * len(dest_lats)
    origin_lon = [origin[1]] * len(dest_lons)
    origin = list(zip(origin_lat, origin_lon))
    dest = list(zip(dest_lats, dest_lons))

    d = haversine_vector(origin, dest, unit=Unit.MILES)

    return d


def create_matrix(
    origin: Tuple[float], dest_lats: List[float], dest_lons: List[float],
):
    """
    creates matrix using optimized matrix processing.

    :origin:        tuple(float); origin coordinates
    :dest_lats:     list-like of floats; latitudes
    :dest_lons:     list-like of floats; longitudes

    returns matrix:list[list, ..., len(origin+lats)-1]
    """
    lats = [origin[0]] + list(dest_lats)
    lons = [origin[1]] + list(dest_lons)

    matrix = []
    for i in range(len(lats)):
        distances = create_vectorized_haversine_li(
            (lats[i], lons[i]), dest_lats=lats, dest_lons=lons
        )

        # must be integer for solver
        distances = np.ceil(distances * 100).astype(int)
        matrix.append(distances)

    return matrix


class DBSCAN:
    def __init__(self, x, y, epsilon=0.5, minpts=2):
        self.epsilon = epsilon
        self.minpts = minpts

    def to_dict(self):
        _dict = {"epsilon": self.epsilon, "minpts": self.minpts}
        try:
            _dict["n X"] = len(self.X)
        except:
            logging.debug("X has not been set.")
        return _dict

    def fit(self, x, y):
        self.X = list(zip(x, y))
        self.clusters = np.zeros(len(self.X), dtype=np.int32)

    @staticmethod
    def get_neighbors(X, i, epsilon):
        neighbors = []
        for j in range(0, len(X)):
            a = np.array(X[i])
            b = np.array(X[j])
            if np.linalg.norm(a - b) < epsilon:
                neighbors.append(j)
        return neighbors

    def build_cluster(self, i, neighbors, cluster):
        self.clusters[i] = cluster
        for j in neighbors:
            if self.clusters[j] == -1:
                self.clusters[j] = cluster
            elif self.clusters[j] == 0:
                self.clusters[j] = cluster
                points = self.get_neighbors(self.X, j, self.epsilon)
                if len(points) >= self.minpts:
                    neighbors += points

    def cluster(self, x=None, y=None):
        if x is None or y is None:
            X = self.X
        else:
            X = list(zip(x, y))

        cluster = 0
        for i in range(0, len(X)):
            if not self.clusters[i] == 0:
                continue
            points = self.get_neighbors(X, i, self.epsilon)
            if len(points) < self.minpts:
                self.clusters[i] = -1
            else:
                cluster += 1
                self.build_cluster(i, points, cluster)


def add_closest_clusters(x: List[float], y: List[float], clusters: List[int]):
    """
    Takes a list of x, a list of y, and a list of clusters to
    process clusters for x, y without an assigned cluster.
    To accomplish this the function calculates the euclidean
    distance to every node with a cluster. It will then assign
    the found node's cluster as its own.
    
    x:        list-like; x coordinates
    y:        list-like; y coordinates
    clusters: list-like; assigned clusters
    
    return list of clusters
    """

    missing_clusters = np.where(clusters == np.nan)[0]

    x_copy = np.array(x, dtype=float)
    x_copy[missing_clusters] = np.inf

    y_copy = np.array(y, dtype=float)
    y_copy[missing_clusters] = np.inf

    for i in missing_clusters:
        x_deltas = abs(x[i] - x_copy)
        y_deltas = abs(y[i] - y_copy)
        deltas = x_deltas + y_deltas

        clusters[i] = clusters[np.argmin(deltas)]

    # return -1 if None
    clusters = np.nan_to_num(clusters, copy=True, nan=-1)

    return clusters


def create_dbscan_basic(x: List[float], y: List[float]):
    """
    Instantiates a basic instance of DBSCAN.

    :x:      list-like of floats; latitudes
    :y:      list-like of floats; longitudes

    returns DBSCAN with .clusters
    """
    epsilon = 0.79585  # approximate degree delta for 50 miles
    minpts = 2  # at least cluster 2

    dbscan = DBSCAN(epsilon, minpts)
    dbscan.fit(x, y)
    dbscan.cluster()

    return dbscan


def create_dbscan_clusters(latitudes: List[float], longitudes: List[float]):
    """
    Uses DBSCAN clustering algorithm to identify groups of nodes based
    on their distance from eachother

    :latitudes:          list-like of floats
    :longitudes:         list-like of floats

    returns clusters:list
    """
    # projecting geocodes
    x = np.array(latitudes, dtype=float) + 90
    y = np.array(longitudes, dtype=float) + 180

    dbscan = create_dbscan_basic(x, y)

    # add those without an assigned cluster
    # to their closest cluster
    clusters = np.where(dbscan.clusters > 0, dbscan.clusters, np.nan)
    clusters = add_closest_clusters(x, y, clusters)

    return clusters
