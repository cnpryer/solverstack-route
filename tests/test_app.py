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
    input_data = jeson.dumps(dict())
    endpoint = '/api/%s/procedure' % __version__
    logging.debug('endpoint: %s.' % endpoint)

    output = client.post(endpoint, data=input_data)

    assert output == input_data