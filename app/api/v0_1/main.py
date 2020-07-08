"""
input: 
{
    "origin_latitude": "",
    "origin_longitude": "",
    "demand_id": [],
    "demand_latitude": [],
    "demand_longitude": [],
    "demand_unit": "",
    "demand_quantity": [],
    "demand_cluster": [],
    "vehicle_max_capacity_quantity": "",
    "vehicles_definitions": []
}
"""
from . import bp
from app import distance, model

from json import loads
from flask import request, jsonify


def parse_for_matrix(data:dict):
    origin_lat, origin_lon = data['origin_latitude'], data['origin_longitude']
    demand_lats = data['demand_latitude']
    demand_lons = data['demand_longitude']

    return distance.create_matrix(
        origin_lat,
        origin_lon,
        demand_lats, 
        demand_lons
    )

def parse_for_demand(data:dict):
    """returns units, unit name"""
    units = data['demand_quantity']
    unit_name = data['demand_unit']

    return units, unit_name

@bp.route('/procedure', methods=['GET', 'POST'])
def main_procedure():
    """
    Main RPC endpoint for passing input data for optimized outputs.
    """

    # request.data is a bytestring
    data = loads(request.data)

    # cluster by location (lat, lon)
    clusters = distance.create_dbscan_clusters(
        data['demand_latitude'], 
        data['demand_longitude']
    )

    # list of lists for all-to-all distances
    matrix = parse_for_matrix(data)

    # describe the demand
    demand, units_name = parse_for_demand(data)

    # manage solve
    solution = model.create_vehicles(matrix, demand, clusters)
    
    # TODO: fix this
    data['vehicle_id'] = list(solution['id'])
    data['stop_num'] = list(solution['stops'])

    return jsonify(data)