from typing import List


def get_stop_distance_factor(matrix: List[List[float]]):
    """
    Calculate average distance between stops (does not include origin).

    :matrix:       list of lists containing all to all distances

    return float
    """
    total_distance = 0
    count = 0
    for n1_li in matrix[1:]:
        for n2 in n1_li[1:]:
            total_distance += n2
            count += 1

    # NOTE: matrix is processed to integers for solver (d * 100)
    distance_factor = (total_distance / 100) / count

    return distance_factor


def get_origin_position_factor(matrix: List[List[float]]):
    """
    Calculate average distance between stops.

    :matrix:       list of lists containing all to all distances

    return float
    """
    # NOTE: matrix is processed to integers for solver (d * 100)
    distance_factor = (sum(matrix[0]) / 100) / len(matrix[0][1:])

    return distance_factor
