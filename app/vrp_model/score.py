def get_load_factors(vehicles: list, demand: list):
    """
    Calculate average shipment size.

    :vehicles:      list of vehicle identities (same order as demand)
    :demand:        list of demand quantities (same order as vehicles)

    return float
    """
    totals = {}
    for i, vehicle in enumerate(vehicles):
        if vehicle in totals:
            totals[vehicle]["sum"] += demand[i]
            totals[vehicle]["count"] += 1
        else:
            totals[vehicle] = {
                "sum": demand[i],
                "count": 1
            }

    load_factors = {
        vehicle: totals[vehicle]["sum"] / totals[vehicle]["count"] 
        for vehicle in totals
    }

    return load_factors