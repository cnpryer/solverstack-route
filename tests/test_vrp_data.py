from . import common


class TestVRPData:
    def test_vrp_origin_data(self, origin):
        origin_lat = origin["latitude"]
        origin_lon = origin["longitude"]

        assert isinstance(origin_lat, float)
        assert -90 < origin_lat < 90

        assert isinstance(origin_lon, float)
        assert -180 < origin_lon < 180

    def test_vrp_demand_data(self, demand):
        demand_unit_name = common.get_vrp_unit_name_basic()

        assert isinstance(demand_unit_name, str)
        assert len(demand_unit_name) > 0
