from . import bp


def get_one_vehicle():
    return 'vehicle placeholder'

@bp.route('/vehicles', methods=['GET'])
def get_many_vehicles():
    return {
        'id': [],
        'max_capacity': [],
        'unit_id': [],
        'asset_class_id': []
    }

def get_one_stop():
    return 'stop placeholder'

@bp.route('/vehicles/stops', methods=['GET'])
def get_many_stops():
    return {
        'id': [],
        'scenario_id': [],
        'vehicle_id': [],
        'stop_num': [],
        'stop_distance': [],
        'unit_id': [],
        'demand_id': []
    }