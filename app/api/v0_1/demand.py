from . import bp


def get_one_demand():
    return 'demand placeholder'

@bp.route('/demand', methods=['GET'])
def get_many_demand():
    return {
        'id': [],
        'units': [],
        'unit_id': [],
        'cluster_id': [],
        'latitude': [],
        'longitude': []
    }