import logging
from typing import List, Tuple

import numpy as np
from haversine import haversine_vector, Unit


def create_vectorized_haversine_li(
    olat: float,
    olon: float,
    dlats: List[float],
    dlons: List[float],
    dist_factor: float = 1.17,
) -> List[float]:
    assert len(dlats) == len(dlons)

    olats: List[float] = [olat] * len(dlats)
    olons: List[float] = [olon] * len(dlons)
    os: List[Tuple[float, float]] = list(zip(olats, olons))
    ds: List[Tuple[float, float]] = list(zip(dlats, dlons))

    ds: List[float] = haversine_vector(os, ds, unit=Unit.MILES)

    # distance factor adjust haversine for theoretical travel difference
    ds *= dist_factor

    return ds


def create_matrix(
    origin_lat: float,
    origin_lon: float,
    dest_lats: List[float],
    dest_lons: List[float],
    int_precision: int = 100,
) -> List[List[int]]:
    """
    creates matrix using optimized matrix processing. distances
    are converted to integers (x*100).

    :_origin:    (origin.lat: float, origin.lon: float)
    :_dests:     list of demands; (demand.lat, demand.lon)

    returns _matrix: list[list, ..., len(origin+dests)]
    """
    LATS: List[float] = [origin_lat] + dest_lats
    LONS: List[float] = [origin_lon] + dest_lons

    assert len(LATS) == len(LONS)

    matrix: List[List[int]] = []
    for i in range(len(LATS)):
        fdistances: List[float] = create_vectorized_haversine_li(
            olat=LATS[i], olon=LONS[i], dlats=LATS, dlons=LONS
        )

        idistances: List[int] = np.ceil(fdistances * int_precision).astype(int)
        matrix.append(idistances)

    return matrix
