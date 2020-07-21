from . import common


def test_vrp_origin_data():
    origin_lat, origin_lon = common.get_vrp_origin_basic()
    assert isinstance(origin_lat, str)
    assert len(origin_lat) > 0

    assert isinstance(origin_lon, str)
    assert len(origin_lon) > 0


def test_vrp_demand_data():
    demand_lats = common.get_vrp_lats_basic()
    demand_lons = common.get_vrp_lons_basic()
    demand_units = common.get_vrp_units_basic()

    assert len(demand_lats) == len(demand_lons)
    assert len(demand_lons) == len(demand_units) - 1

    demand_unit_name = common.get_vrp_unit_name_basic()

    assert isinstance(demand_unit_name, str)
    assert len(demand_unit_name) > 0
