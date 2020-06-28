import logging


def get_vrp_origin():
    """returns lat:str, lon:str"""
    lat, lon = '41.4191', '-87.7748'
    logging.debug(f'origin lat: {lat}, lon: {lon}')

    return lat, lon

def get_vrp_lats():
    lats =  ['39.6893', '39.6893', '43.7266', '40.2932', '39.1594', '38.2306',
        '40.2874']
    logging.debug(f'demand lats: {lats}')

    return lats

def get_vrp_lons():
    lons =  ['-86.3919', '-86.3919', '-87.8242', '-83.0723', '-84.35655', '-85.7905', 
        '-84.1622']
    logging.debug(f'demand lons: {lons}')

    return lons

def get_vrp_unit_name():
    name = 'pallets'
    logging.debug(f'unit name: {name}')
    
    return name

def get_vrp_units():
    units = ['5', '10', '2', '4', '12', '6', '14']
    logging.debug(f'demand units: {units}')

    return units

def get_vrp_data():
    origin_lat, origin_lon = get_vrp_origin()

    return {
        'origin_latitude': origin_lat,
        'origin_longitude': origin_lat,
        'demand': {
            'latitude': get_vrp_lats(),
            'longitude': get_vrp_lons(),
            'units': get_vrp_units(),
            'unit_name': get_vrp_unit_name(),
            'cluster': None #
        },
        'vehicles': None
    }

VRP_DATA = get_vrp_data()