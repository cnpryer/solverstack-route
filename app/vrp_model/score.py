def get_totals(vehicles: list, demand: list):
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
            totals[vehicle] = {
                "sum": demand[i],
                "count": 1
            }
    
    return totals

def get_load_factor(vehicles: list, demand: list):
    """
    Calculate average shipment size.

    :vehicles:      list of vehicle identities (same order as demand)
    :demand:        list of demand quantities (same order as vehicles)

    return float
    """
    totals = get_totals(vehicles, demand)
    load_factor = sum(demand) / len(list(totals))
    
    return load_factor

def get_aggregation(vehicles: list, demand: list):
    """
    Calculate the percent of demand aggregated.

    :vehicles:      list of vehicle identities (same order as demand)
    :demand:        list of demand quantities (same order as vehicles)

    return float
    """
    totals = get_totals(vehicles, demand)
    total_aggregation = sum([
        totals[vehicle]["count"]
        for vehicle in totals if totals[vehicle]["count"] > 1 
    ])

    aggregation = total_aggregation / len(demand)

    return aggregation