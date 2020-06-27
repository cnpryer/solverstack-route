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