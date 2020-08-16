import pytest
from app.vrp_model import distance

from . import common


class TestDistance:
    @pytest.fixture()
    def matrix(self):
        pass

    def test_matrix_processing(self, origin, latitudes, longitudes):
        origin_lat = origin["latitude"]
        origin_lon = origin["longitude"]
        matrix = distance.create_matrix((origin_lat, origin_lon), latitudes, longitudes)

        assert len(matrix) == len(latitudes) + 1

    def test_cluster_processing(self, latitudes, longitudes):
        """Test creation of clusters"""
        assert len(latitudes) == len(longitudes)

        clusters = distance.create_dbscan_clusters(latitudes, longitudes)

        assert len(latitudes) == len(clusters)
