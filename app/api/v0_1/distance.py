import numpy as np


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
        matrix.append(distances)
    
    return matrix