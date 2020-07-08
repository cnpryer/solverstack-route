from app import distance

import logging
import os

from pandas import read_csv


TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
CSV_TESTING_FILENAME = 'vrp_testing_data.csv'
CSV_TESTING_FILEPATH = os.path.join(TEST_ROOT, CSV_TESTING_FILENAME)

def get_csv():
    logging.debug(f'filepath: {CSV_TESTING_FILEPATH}.')

    return read_csv(CSV_TESTING_FILEPATH)

TESTING_CSV_DF = get_csv()

def get_vrp_origin_basic():
    """returns lat:str, lon:str"""
    lat, lon = '41.4191', '-87.7748'
    logging.debug(f'origin lat: {lat}, lon: {lon}.')

    return lat, lon

def get_vrp_lats_basic():
    lats =  ['39.6893', '39.6893', '43.7266', '43.7266', '38.2306', '38.2306',
        '43.7266']
    logging.debug(f'demand lats: {lats}.')

    return lats

def get_vrp_lons_basic():
    lons =  ['-86.3919', '-86.3919', '-87.8242', '-87.8242', '-84.35655', '-84.35655', 
        '-87.8242']
    logging.debug(f'demand lons: {lons}.')

    return lons

def get_vrp_unit_name_basic():
    name = 'pallets'
    logging.debug(f'unit name: {name}.')
    
    return name

def get_vrp_units_basic():
    """demand units must have 0 for origin node"""
    units = ['0', '5', '10', '2', '4', '12', '6', '14']
    logging.debug(f'demand units: {units}')

    return units

def get_vrp_lats_csv():
    lats =  TESTING_CSV_DF.latitude.astype(str).tolist()
    logging.debug(f'demand lats: {lats}')

    return lats

def get_vrp_lons_csv():
    lons =  TESTING_CSV_DF.longitude.astype(str).tolist()
    logging.debug(f'demand lons: {lons}')

    return lons

def get_vrp_unit_name_csv():
    name = 'pallets'
    logging.debug(f'unit name: {name}')
    
    return name

def get_vrp_units_csv():
    """demand units must have 0 for origin node"""
    units = [0] + TESTING_CSV_DF.pallets.fillna(1).astype(str).tolist()
    logging.debug(f'demand units: {units}')

    return units

def get_vrp_data_basic():
    origin_lat, origin_lon = get_vrp_origin_basic()

    return {
        'origin_latitude': origin_lat,
        'origin_longitude': origin_lat,
        'demand_latitude': get_vrp_lats_basic(),
        'demand_longitude': get_vrp_lons_basic(),
        'demand_unit': get_vrp_unit_name_basic(),
        'demand_quantity': get_vrp_units_basic(),
        'demand_cluster': None, # TODO
        'vehicle_max_capacity_quantity': '26',
        'vehicle_definitions': None # TODO
    }

def get_vrp_data_csv():
    # TODO: abstract json def
    origin_lat, origin_lon = get_vrp_origin_basic()

    return {
        'origin_latitude': origin_lat,
        'origin_longitude': origin_lat,
        'demand_latitude': get_vrp_lats_csv(),
        'demand_longitude': get_vrp_lons_csv(),
        'demand_quantity': get_vrp_units_csv(),
        'demand_unit': get_vrp_unit_name_basic(),
        'demand_cluster': None, # TODO
        'vehicle_max_capacity_quantity': '26',
        'vehicle_definitions': None # TODO
    }

def get_matrix_basic():
    origin_lat, origin_lon = get_vrp_origin_basic()
    demand_lats = get_vrp_lats_basic()
    demand_lons = get_vrp_lons_basic()

    return distance.create_matrix(
        origin_lat,
        origin_lon,
        demand_lats, 
        demand_lons
    )

def get_dbscan_clusters_basic():
    lats = get_vrp_lats_basic()
    lons = get_vrp_lons_basic()

    return distance.create_dbscan_clusters(lats, lons)

def get_matrix_csv():
    origin_lat, origin_lon = get_vrp_origin_basic()
    demand_lats = get_vrp_lats_csv()
    demand_lons = get_vrp_lons_csv()

    return distance.create_matrix(
        origin_lat,
        origin_lon,
        demand_lats, 
        demand_lons
    )

def get_dbscan_clusters_csv():
    lats = get_vrp_lats_csv()
    lons = get_vrp_lons_csv()

    return distance.create_dbscan_clusters(lats, lons)

VRP_DATA = get_vrp_data_csv()