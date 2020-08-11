import logging
import random

import pytest

from app import create_app
from app.vrp_model import distance
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture(scope="session")
def client():
    yield create_app(TestConfig).test_client()


@pytest.fixture
def demand():
    return [
        {
            "latitude": random.uniform(-90, 90),
            "longitude": random.uniform(-180, 180),
            "quantity": random.randint(0, 1000),
        }
        for i in range(10)
    ]
    pass


@pytest.fixture
def origin():
    """returns lat:float, lon:float"""
    lat, lon = 41.4191, -87.7748
    logging.debug(f"origin lat: {lat}, lon: {lon}.")

    return {"latitude": lat, "longitude": lon}


@pytest.fixture()
def clusters(latitudes, longitudes):
    """Return list of clusters"""

    return distance.create_dbscan_clusters(latitudes, longitudes)


@pytest.fixture()
def latitudes():
    lats = [39.6893, 39.6893, 43.7266, 43.7266, 38.2336, 38.2306, 43.7266]
    logging.debug(f"demand lats: {lats}.")

    return lats


@pytest.fixture()
def longitudes():
    lons = [-86.3919, -86.3919, -87.8242, -87.8242, -84.35655, -84.35655, -87.8242]
    logging.debug(f"demand lons: {lons}.")

    return lons


@pytest.fixture()
def quantities():
    """demand units must have 0 for origin node"""
    units = ["0", "5", "10", "2", "4", "12", "6", "14"]
    logging.debug(f"demand units: {units}")

    return units
