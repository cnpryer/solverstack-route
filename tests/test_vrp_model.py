import numpy as np
import pytest

from app.vrp_model import model, distance
from app.vrp_model.scoring import output_scoring


class TestVRPModel:
    MAX_VEHICLE_CAPACITY_UNITS = 26
    MAX_SEARCH_SECONDS = 30

    @pytest.mark.filterwarnings
    def test_create_vehicles(self, clusters, origin, latitudes, longitudes, quantities):
        origin_lat = origin["latitude"]
        origin_lon = origin["longitude"]
        demand = [int(d) for d in quantities]
        vehicles = model.create_routes(
            origin_lat=origin_lat,
            origin_lon=origin_lon,
            dest_lats=latitudes,
            dest_lons=longitudes,
            demand_quantities=quantities,
            max_vehicle_capacity=26,
        )

        load_factor = output_scoring.get_load_factor(vehicles["id"], demand[1:])

        # assert load_factor <= self.MAX_VEHICLE_CAPACITY_UNITS

        assert vehicles["id"] is not None

    @pytest.mark.filterwarnings
    def test_vrp_bundle_case(self, origin, latitudes, longitudes, quantities):

        origin_lat = origin["latitude"]
        origin_lon = origin["longitude"]
        demand = [int(d) for d in quantities]
        vehicles = model.create_routes(
            origin_lat=origin_lat,
            origin_lon=origin_lon,
            dest_lats=latitudes,
            dest_lons=longitudes,
            demand_quantities=quantities,
            max_vehicle_capacity=26,
        )

        if not vehicles:
            return None

        assert vehicles["id"] is not None
