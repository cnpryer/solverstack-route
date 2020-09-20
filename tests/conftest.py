from . import common
from app import create_app
from app.vrp_model import distance, cluster
from config import Config

import logging
import random
import pytest
from flask_jwt_extended import create_access_token


TEST_USER: dict = {"id": 1, "username": "test", "password": "password"}


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture()
def auth_header():
    app = create_app(TestConfig)

    with app.app_context():
        token = create_access_token(TEST_USER)

    headers: dict = {"Authorization": "Bearer {}".format(token)}

    return headers


@pytest.fixture(scope="session")
def client():
    yield create_app(TestConfig).test_client()


@pytest.fixture
def demand():
    return [
        {
            "id": i,
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
            "quantity": random.randint(0, 26),
        }
        for i in range(10)
    ]


@pytest.fixture
def origin():
    """returns lat:float, lon:float"""
    lat, lon = 41.4191, -87.7748
    logging.debug(f"origin lat: {lat}, lon: {lon}.")

    return {"id": 1, "latitude": lat, "longitude": lon}


@pytest.fixture()
def clusters(latitudes, longitudes):
    """Return list of clusters"""

    return cluster.create_dbscan_clusters(latitudes, longitudes)


@pytest.fixture()
def latitudes():
    lats = common.TESTING_CSV_DF.latitude.tolist()
    logging.debug(f"demand lats: {lats}.")

    return lats


@pytest.fixture()
def longitudes():
    lons = common.TESTING_CSV_DF.longitude.tolist()
    logging.debug(f"demand lons: {lons}.")

    return lons


@pytest.fixture()
def quantities():
    """demand units must have 0 for origin node"""
    units = [0] + common.TESTING_CSV_DF.pallets.tolist()
    logging.debug(f"demand units: {units}")

    return units
