import numpy as np
import pytest

from app.vrp_model import model, distance


class TestVRPModel:
    MAX_VEHICLE_CAPACITY_UNITS = 26
    MAX_SEARCH_SECONDS = 30

    @pytest.mark.filterwarnings
    def test_create_vehicles(self, clusters, origin, latitudes, longitudes, quantities):
        origin_lat = origin["location"]["latitude"]
        origin_lon = origin["location"]["longitude"]
        matrix = distance.create_matrix(origin_lat, origin_lon, latitudes, longitudes)

        demand = [int(d) for d in quantities]
        vehicles = model.create_vehicles(matrix, demand, np.array(clusters))

        assert len(vehicles["id"]) == len(clusters)

    @pytest.mark.filterwarnings
    def test_vrp_bundle_case(self, origin, latitudes, longitudes, quantities):

        origin_lat = origin["location"]["latitude"]
        origin_lon = origin["location"]["longitude"]
        matrix = distance.create_matrix(origin_lat, origin_lon, latitudes, longitudes)

        demand = [int(d) for d in quantities]
        bndl = model.VrpBasicBundle(
            matrix=matrix,
            demand=demand,
            max_vehicle_capacity_units=26,
            max_search_seconds=30,
        )

        assert len(bndl.run().get_solution()["id"]) == len(latitudes)
