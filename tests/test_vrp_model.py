from . import common
from app import model

import numpy as np
import pytest


CLUSTERS = common.get_dbscan_clusters_basic()
MATRIX = common.get_matrix_basic()
DEMAND = [int(d) for d in common.get_vrp_units_basic()]
MAX_VEHICLE_CAPACITY_UNITS = 26
MAX_SEARCH_SECONDS = 30
CLUSTERS = common.get_dbscan_clusters_basic()

@pytest.mark.filterwarnings
def test_create_vehicles():
    vehicles = model.create_vehicles(MATRIX, DEMAND, np.array(CLUSTERS))

    assert len(vehicles['id']) == len(CLUSTERS)

@pytest.mark.filterwarnings
def test_vrp_bundle_case():
    bndl = model.VrpBasicBundle(
        matrix=MATRIX,
        demand=DEMAND,
        max_vehicle_capacity_units=26,
        max_search_seconds=30
    )

    lats = common.get_vrp_lats_basic()

    assert len(bndl.run().get_solution()['id']) == len(lats)
