from . import bp
from app import distance, model

from json import loads
from flask import request, jsonify


def parse_json(json: dict):
    # TODO: require specific format/naming
    data = {
        "origin_latitude": json["origin_latitude"],
        "origin_longitude": json["origin_longitude"],
        "unit": json["unit"],
        "demand_latitude": [],
        "demand_longitude": [],
        "demand_quantity": [],
        "demand_cluster": [],
        "vehicle_max_capacity_quantity": json["vehicle_max_capacity_quantity"],
        "vehicle_definitions": json["vehicle_definitions"],
    }

    for i in range(len(json["demand"])):
        row = json["demand"][i]
        print(row)

        data["demand_latitude"].append(row["latitude"])
        data["demand_longitude"].append(row["longitude"])
        data["demand_quantity"].append(row[data["unit"]])

    return data


@bp.route("/vrp", methods=["GET", "POST"])
def vrp_procedure():
    """
    Main RPC endpoint for passing input data for optimized outputs.

    :origin_latitude:               float
    :origin_longitude:              float
    :unit:                          string; maps to unit of measure 
                                    key from POST
    :demand:                        list-like; contains ordered demand
                                    nodes represented as dict-like 
                                    objects
          :demand_longitude:        float
          :demand_quantity:         int
          :demand_cluster:          int
    :vehicle_max_capacity_quantity: int
    :vehicle_definitions':          list-like; int for vehicle max
                                    capacity overrides                                 
    """
    # request.data is a bytestring
    data = parse_json(loads(request.data))

    # cluster by location (lat, lon)
    clusters = distance.create_dbscan_clusters(
        data["demand_latitude"], data["demand_longitude"]
    )

    # list of lists for all-to-all distances
    matrix = distance.create_matrix(
        data["origin_latitude"],
        data["origin_longitude"],
        data["demand_latitude"],
        data["demand_longitude"],
    )

    # manage solve
    solution = model.create_vehicles(matrix, ["0"] + data["demand_quantity"], clusters)

    # TODO: fix this
    data["vehicle_id"] = list(solution["id"])
    data["stop_num"] = list(solution["stops"])

    return jsonify(data)
