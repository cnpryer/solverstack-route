"""
input: 
{
"origin_latitude": "",
"origin_longitude": "",
"demand": {
    "latitude": [],
    "longitude": [],
    "units": [], # this will change with future iterations
    "unit_name": "",
    "max_vehicle_capacity_units": "",
    "cluster": []
},
"vehicles": [] # optional
}
"""
from . import bp, distance, model
from json import loads
from flask import request, jsonify


def parse_for_matrix(data:dict):
    origin_lat, origin_lon = data['origin_latitude'], data['origin_longitude']
    demand_lats = data['demand']['latitude']
    demand_lons = data['demand']['longitude']

    return distance.create_matrix(
        origin_lat,
        origin_lon,
        demand_lats, 
        demand_lons
    )

def parse_for_demand(data:dict):
    """returns units, unit name"""
    units = data['demand']['units']
    unit_name = data['demand']['unit_name']

    return units, unit_name

@bp.route('/procedure', methods=['GET', 'POST'])
def main_procedure():
    """
    Main RPC endpoint for passing input data for optimized outputs.
    """

    # request.data is a bytestring
    data = loads(request.data)

    matrix = parse_for_matrix(data)
    demand, units_name = parse_for_demand(data)
    bndl = model.VrpBasicBundle(
        matrix=matrix,
        demand=demand,
        max_vehicle_capacity_units=int(data['max_vehicle_capacity_units'])
    )

    solution = bndl.run().get_solution()

    return jsonify(solution)