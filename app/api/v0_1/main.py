from json import loads
from typing import List

from connexion import request
from flask import jsonify, make_response

# from app.api.models.inline_response200 import InlineResponse200  # noqa: E501
from app.api.models.invalid_usage_error import InvalidUsageError  # noqa: E501
from app.api.v0_1.models.procedure_request import ProcedureRequest  # noqa: E501
from app.api.v0_1.models.solution_response import SolutionResponse  # noqa: E501
from app.vrp_model import distance, model

from . import bp


@bp.route("/vrp", methods=["POST"])
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
    :demand_longitude:              float
    :demand_quantity:               int
    :demand_cluster:                int
    :vehicle_max_capacity_quantity: int
    :vehicle_definitions':          list-like; int for vehicle max
                                    capacity overrides                                 
    """

    if request.is_json:
        body = ProcedureRequest.from_dict(request.get_json())  # noqa: E501
    else:
        return make_response(
            jsonify(
                InvalidUsageError(
                    f"Incorrect request format! Content type received '{request.content_type}' instead of 'application/json'"
                )
            ),
            400,
        )
    demands = body.demands

    demand_latitudes = [demand.location.latitude for demand in demands]
    demand_longitudes = [demand.location.longitude for demand in demands]
    demand_quantities = [demand.quantity for demand in demands]

    # cluster by location (lat, lon)
    clusters = distance.create_dbscan_clusters(demand_latitudes, demand_longitudes)

    origin = body.origin
    # list of lists for all-to-all distances
    matrix = distance.create_matrix(
        (origin.location.latitude, origin.location.longitude,),
        demand_latitudes,
        demand_longitudes,
    )

    # manage solve
    solutions = model.create_vehicles(matrix, ["0"] + demand_quantities, clusters)

    response = {
        "origin": origin,
        "unit": body.unit,
        "vehicle_capacity": body.vehicle_capacity,
    }

    response_solutions = [
        {
            "cluster": clusters[i],
            "demand": demand,
            "stop_id": solutions["stops"][i],
            "vehicle_id": solutions["id"][i],
        }
        for i, demand in enumerate(demands)
    ]
    response["solutions"] = response_solutions

    return jsonify(response)
