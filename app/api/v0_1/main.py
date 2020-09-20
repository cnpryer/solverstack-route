from . import bp

# from app.api.models.inline_response200 import InlineResponse200  # noqa: E501
from app.api.models.invalid_usage_error import InvalidUsageError  # noqa: E501
from app.api.v0_1.models.procedure_request import ProcedureRequest  # noqa: E501
from app.api.v0_1.models.routes_response import RoutesResponse  # noqa: E501
from app.vrp_model import model

import requests
from json import loads
from typing import List
from connexion import request
from flask import jsonify, make_response


CRUD_URL: str = "http://localhost:5004/api/v0.1/route"


@bp.route("/route", methods=["POST"])
def route_procedure():
    """
    Main RPC endpoint for passing input data for optimized outputs.

    :stack_id:                      integer
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
    demand = body.demand

    stack_id = body.stack_id

    demand_ids = [int(d.id) for d in demand]
    demand_latitudes = [float(d.latitude) for d in demand]
    demand_longitudes = [float(d.longitude) for d in demand]
    demand_quantities = [d.quantity for d in demand]
    origin = body.origin

    # manage solve
    routes = model.create_vehicles(
        origin_lat=origin.latitude,
        origin_lon=origin.longitude,
        dest_lats=demand_latitudes,
        dest_lons=demand_longitudes,
        demand_quantities=demand_quantities,
        max_vehicle_capacity=body.vehicle_capacity,
    )

    default_response = {
        "stack_id": stack_id,
        "origin": origin,
        "demand": demand,
        "unit": body.unit,
        "vehicle_capacity": body.vehicle_capacity,
    }

    if len(routes["stops"]) == 0:
        default_response["routes"] = routes

        return make_response(jsonify(default_response), 200)

    results = [
        {
            "depot_id": origin.id,
            "demand_id": demand[i].id,
            "stop_number": routes["stops"][i],
            "vehicle_id": routes["id"][i],
        }
        for i in range(len(demand))
    ]

    try:

        if not request.headers.get("Authorization"):
            raise ValueError("Unauthroized request")

        input_data: dict = {"stack_id": stack_id, "routes": results}
        response = requests.post(CRUD_URL, headers=request.headers, json=input_data)

        if response.status_code not in [200, 201]:
            raise ValueError("Integration error")

        return make_response(jsonify(loads(response.text)), 200)

    except:

        default_response["routes"] = results
        return make_response(jsonify(default_response), 200)
