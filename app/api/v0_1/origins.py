from . import bp


@bp.route('/origin', methods=['GET'])
def get_one_origin():
    return {
        'id': 0,
        'latitude': 0.,
        'longitude': 0.
    }