from . import bp
from app import distance, model

from json import loads
from flask import request, jsonify


def parse_json(json:dict):
    # TODO: require specific format/naming
    data = {
        'origin_latitude': json['origin_latitude'],
        'origin_longitude': json['origin_longitude'],
        'unit': json['unit'],
        'demand_latitude': [],
        'demand_longitude': [],
        'demand_quantity': [],
        'demand_cluster': [],
        'vehicle_max_capacity_quantity': json['vehicle_max_capacity_quantity'],
        'vehicle_definitions': json['vehicle_definitions']
    }

    for i in range(len(json['demand'])):
        row = json['demand'][i]
        print(row)

        data['demand_latitude'].append(row['latitude'])
        data['demand_longitude'].append(row['longitude'])
        data['demand_quantity'].append(row[data['unit']])

    return data

@bp.route('/procedure', methods=['GET', 'POST'])
def main_procedure():
    """
    Main RPC endpoint for passing input data for optimized outputs.
    """

    # request.data is a bytestring
    data = parse_json(loads(request.data))

    # cluster by location (lat, lon)
    clusters = distance.create_dbscan_clusters(
        data['demand_latitude'], 
        data['demand_longitude']
    )

    # list of lists for all-to-all distances
    matrix = distance.create_matrix(
        data['origin_latitude'],
        data['origin_longitude'],
        data['demand_latitude'], 
        data['demand_longitude']
    )

    # manage solve
    solution = model.create_vehicles(matrix, ['0'] + data['demand_quantity'], clusters)
    
    # TODO: fix this
    data['vehicle_id'] = list(solution['id'])
    data['stop_num'] = list(solution['stops'])

    return jsonify(data)