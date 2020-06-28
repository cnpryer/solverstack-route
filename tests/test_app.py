from . import common
from app.api import __version__
import logging

from app import create_app
from app.api.v0_1 import distance
from config import Config

import pytest
import json


VRP_DATA = common.VRP_DATA

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

@pytest.fixture
def client():
    yield create_app(TestConfig).test_client()

def test_vrp_origin_data():
    origin_lat, origin_lon = common.get_vrp_origin()
    assert isinstance(origin_lat, str)
    assert len(origin_lat) > 0

    assert isinstance(origin_lon, str)
    assert len(origin_lon) > 0

def test_vrp_demand_data():
    demand_lats = common.get_vrp_lats()
    demand_lons = common.get_vrp_lons()
    demand_units = common.get_vrp_units()
    
    assert len(demand_lats) == len(demand_lons)
    assert len(demand_lons) == len(demand_units)

    demand_unit_name = common.get_vrp_unit_name()

    assert isinstance(demand_unit_name, str)
    assert len(demand_unit_name) > 0

def test_matrix_processing():
    origin_lat, origin_lon = common.get_vrp_origin()
    demand_lats = common.get_vrp_lats()
    demand_lons = common.get_vrp_lons()

    matrix = distance.create_matrix(
        origin_lat,
        origin_lon,
        demand_lats, 
        demand_lons
    )

    assert len(matrix) == len(demand_lats) + 1
    

def test_main_procedure(client):
    input_data = VRP_DATA
    logging.debug(f'input data : {input_data}')

    endpoint = f'/api/{__version__}/procedure'
    logging.debug(f'endpoint: {endpoint}')

    response = client.post(endpoint, json=input_data)
    output = json.loads(response.get_data())

    assert output == input_data