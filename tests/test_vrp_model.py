from . import common
from app.api.v0_1 import distance, model

import numpy as np
import pytest


CLUSTERS = common.get_dbscan_clusters()
MATRIX = common.get_matrix()
DEMAND = [int(d) for d in common.get_vrp_units()]
MAX_VEHICLE_CAPACITY_UNITS = 26
MAX_SEARCH_SECONDS = 30
CLUSTERS = common.get_dbscan_clusters()

@pytest.mark.filterwarnings
def test_create_vehicles():
    vehicles = model.create_vehicles(MATRIX, DEMAND, np.array(CLUSTERS))

    assert len(vehicles) == len(CLUSTERS)

@pytest.mark.filterwarnings
def test_vrp_bundle_case():
    bndl = model.VrpBasicBundle(
        matrix=MATRIX,
        demand=DEMAND,
        max_vehicle_capacity_units=26,
        max_search_seconds=30
    )

    lats = common.get_vrp_lats()

    assert len(bndl.run().get_solution()) == len(lats)
