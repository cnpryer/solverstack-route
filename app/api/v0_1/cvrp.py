from . import bp

@bp.route('/demand', methods=['GET', 'POST'])
def demand():
    return 'demand placeholder'

@bp.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    return 'vehicles placeholder'

@bp.route('/stops', methods=['GET'])
def stops():
    return 'stops placeholder'

@bp.route('/origins', methods=['GET', 'POST'])
def origins():
    return 'origins placeholder'
