from typing import List


def get_totals(vehicles: List[int], demand: List[float]):
    """
    Create dict of sum and count demand per vehicle.

    :vehicles:      list of vehicle identities (same order as demand)
    :demand:        list of demand quantities (same order as vehicles)

    return dict
    """
    totals = {}
    for i, vehicle in enumerate(vehicles):
        if vehicle in totals:
            totals[vehicle]["sum"] += demand[i]
            totals[vehicle]["count"] += 1
        else:
            totals[vehicle] = {"sum": demand[i], "count": 1}

    return totals


def get_routes(vehicles: List[int], stops: List[int]):
    """
    Create dict of vehicles (key) and their routes (value).

    :vehicles:      list of vehicle identities (same order as demand)
    :stops:        list of stop numbers (same order as vehicles)

    return dict
    """
    counts = {}
    for vehicle in vehicles:
        if vehicle in counts:
            counts[vehicle] += 1
        else:
            counts[vehicle] = 1

    routes = {}
    for i, vehicle in enumerate(vehicles):
        if vehicle not in routes:
            routes[vehicle] = [None for j in range(counts[vehicle])]

        routes[vehicle][int(stops[i]) - 1] = i

    return routes


def get_load_factor(vehicles: List[int], demand: List[float]):
    """
    Calculate average shipment size.

    :vehicles:      list of vehicle identities (same order as demand)
    :demand:        list of demand quantities (same order as vehicles)

    return float
    """
    totals = get_totals(vehicles, demand)
    load_factor = sum(demand) / len(list(totals))

    return load_factor


def get_aggregation(vehicles: List[int], demand: List[float]):
    """
    Calculate the percent of demand aggregated.

    :vehicles:      list of vehicle identities (same order as demand)
    :demand:        list of demand quantities (same order as vehicles)

    return float
    """
    totals = get_totals(vehicles, demand)
    total_aggregation = sum(
        [totals[vehicle]["count"] for vehicle in totals if totals[vehicle]["count"] > 1]
    )

    aggregation = total_aggregation / len(demand)

    return aggregation


def get_total_distance(
    routes: dict, matrix: List[List[float]], include_origin: bool = True
):
    """
    Calulate total distance on a route.

    :routes:          dict of vehicle routes with ordered stop indicies
    :matrix:          list of lists of travel distances between nodes (includes origin)
    :include_origin:  include travel distance from and to origins in calculation

    return float
    """
    total_distance = 0
    for vehicle in routes:
        for i in range(len(routes[vehicle]) - 1):
            total_distance += matrix[routes[vehicle][i] + 1][routes[vehicle][i + 1] + 1]

        if include_origin:
            total_distance += matrix[0][routes[vehicle][0]]
            total_distance += matrix[routes[vehicle][-1]][0]

    return total_distance


def get_stop_distance_factor(
    vehicles: List[int], stops: List[int], matrix: List[List[float]]
):
    """
    Calculate average stop travel distance not including origin depart or return. 
    len(vehicles) == len(stops) == len(matrix[1:]li[1:]). matrix contains origin node position.

    :vehicles:      list of vehicle identifiers
    :stops:         list of stop numbers
    :matrix:        list of lists of travel distances between nodes (includes origin)
    
    return float
    """
    routes = get_routes(vehicles, stops)
    total_distance = get_total_distance(routes, matrix, include_origin=False)

    # NOTE: distance matrix is processed to integers using d * 100
    distance_factor = (total_distance / 100) / len(stops)

    return distance_factor


def get_route_distance_factor(
    vehicles: List[int], stops: List[int], matrix: List[List[float]]
):
    """
    Calculate average vehicle route travel distance including origin depart and return. 
    len(vehicles) == len(stops) == len(matrix[1:]li[1:]). matrix contains origin node position.

    :vehicles:      list of vehicle identifiers
    :stops:         list of stop numbers
    :matrix:        list of lists of travel distances between nodes (includes origin)
    
    return float
    """
    routes = get_routes(vehicles, stops)
    total_distance = get_total_distance(routes, matrix)

    # NOTE: distance matrix is processed to integers using d * 100
    distance_factor = (total_distance / 100) / (len(stops) + (len(routes) * 2))

    return distance_factor
