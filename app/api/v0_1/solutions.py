from . import bp


@bp.route('/solution', methods=['GET'])
def get_one_solution():
    return {
        'demand_id': [],
        'origin_id': [],
        'vehicle_id': [],
        'stop_num': [],
        '[uom name]': []
    }