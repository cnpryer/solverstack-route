import numpy as np
import logging


def create_vectorized_haversine_li(origin_lat:float, origin_lon:float, dest_lons:list, 
dest_lats:list, unit:str='mi'):
    """
    haversine formula: https://en.wikipedia.org/wiki/Haversine_formula

    TODO: validate formula (w. tests)
    returns distances:list
    """
    dlat = dest_lats - origin_lat
    dlon = dest_lons - origin_lon

    a = np.sin(dlat/2)**2 + np.cos(origin_lat) * np.cos(dest_lats) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    r = {
        'mi': 3956,
        'km': 6371
    }[unit]

    return c * r

def create_matrix(origin_lat:float, origin_lon:float, dest_lats:list, dest_lons: list):
    """
    creates matrix using optimized matrix processing.

    :origin:        ['latitude', 'longitude']
    :lats:          ['lat', 'lat', 'lat', ...]
    :lons:          ['lon', 'lon', 'lon', ...]

    returns matrix:list[list, ..., len(origin+lats)-1]
    """
    origin_lat = np.radians([float(origin_lat)])[0]
    origin_lon = np.radians([float(origin_lon)])[0]

    lats = np.array([origin_lat] + dest_lats, dtype=float)
    lons = np.array([origin_lon] + dest_lons, dtype=float)

    matrix = []
    for i in range(len(lats)):
        distances = create_vectorized_haversine_li(
            origin_lat=lats[i],
            origin_lon=lons[i],
            dest_lats=lats,
            dest_lons=lons
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
        _dict = {'epsilon': self.epsilon, 'minpts': self.minpts}
        try:
            _dict['n X'] = len(self.X)
        except:
            logging.debug('X has not been set.')
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
            if np.linalg.norm(a-b) < epsilon:
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

def add_closest_clusters(x:list, y:list, clusters:list):
    """
    Takes a list of x, a list of y, and a list of clusters to
    process clusters for x, y without an assigned cluster.
    To accomplish this the function calculates the euclidean
    distance to every node with a cluster. It will then assign
    the found node's cluster as its own.
    
    x: list-like of x coordinates
    y: list-like of y coordinates
    clusters: list-like of clusters assigned
    
    return list of clusters
    """
    
    missing_clusters = np.where(clusters == np.nan)[0]
    has_clusters = np.where(clusters != np.nan)[0]
    
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

def create_dbscan_basic(x:list, y:list):
    epsilon = 0.79585 # approximate degree delta for 50 miles
    minpts = 2 # at least cluster 2

    dbscan = DBSCAN(epsilon, minpts)
    dbscan.fit(x, y)
    dbscan.cluster()
    
    return dbscan

def create_dbscan_clusters(latitudes:list, longitudes:list):
    """
    Uses DBSCAN clutering algorithm to identify groups of nodes based
    on their distance from eachother

    :latitudes:          ['lat', ...] destination lats
    :longitudes:         ['lon', ...] destination lons

    returns clusters:list
    """
    # projecting geocodes
    x = np.array(latitudes, dtype=float) + 180
    y = np.array(longitudes, dtype=float) + 180

    dbscan = create_dbscan_basic(x, y)
    
    # add those without an assigned cluster
    # to their closest cluster
    clusters = np.where(dbscan.clusters > 0, dbscan.clusters, np.nan)
    clusters = add_closest_clusters(x, y, clusters)
    
    return clusters