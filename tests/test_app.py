import json
import logging

import pytest

from app import create_app
from app.api import __version__
from config import Config

from . import common

VRP_DATA = common.VRP_DATA


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture
def client():
    yield create_app(TestConfig).test_client()


@pytest.mark.filterwarnings
def test_main_procedure(client):
    input_data = VRP_DATA
    logging.debug(f"input data : {input_data}")

    endpoint = f"/api/{__version__}/vrp"
    logging.debug(f"endpoint: {endpoint}")

    response = client.post(endpoint, json=input_data)
    output = json.loads(response.get_data())

    assert len(output["vehicle_id"]) == len(VRP_DATA["demand"])
