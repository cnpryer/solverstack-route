from . import common
from app.api import __version__
import logging

from app import create_app
from config import Config

import pytest
import json


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

@pytest.fixture
def client():
    yield create_app(TestConfig).test_client()

def test_main_procedure(client):
    input_data = json.dumps(common.get_vrp_data())
    logging.debug(f'input data : {input_data}')

    endpoint = f'/api/{__version__}/procedure'
    logging.debug(f'endpoint: {endpoint}')

    response = client.post(endpoint, json=input_data)
    output = json.loads(response.get_data())

    assert output == input_data