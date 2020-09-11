import pytest
from app.vrp_model import distance

from . import common


class TestDistance:
    @pytest.fixture()
    def matrix(self):
        pass

    def test_matrix_processing(self):
        origin_lat = 37.0
        origin_lon = -79.0

        latitudes = [40.1717, 33.9883, 33.9163, 39.8295, 39.9474, 33.9321, 40.8219]
        longitudes = [-80.256, -83.8795, -84.8278, -75.4354, -75.1473, -83.3525, -74.42]
        matrix = distance.create_matrix((origin_lat, origin_lon), latitudes, longitudes)

        assert len(matrix) == len(latitudes) + 1

    def test_cluster_processing(self):
        """Test creation of clusters"""
        latitudes = [40.1717, 33.9883, 33.9163, 39.8295, 39.9474, 33.9321, 40.8219]
        longitudes = [-80.256, -83.8795, -84.8278, -75.4354, -75.1473, -83.3525, -74.42]

        assert len(latitudes) == len(longitudes)

        clusters = distance.create_dbscan_clusters(latitudes, longitudes)

        assert len(latitudes) == len(clusters)
