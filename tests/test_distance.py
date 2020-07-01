from . import common


def test_matrix_processing():
    matrix = common.get_matrix()
    demand_lats = common.get_vrp_lats()

    assert len(matrix) == len(demand_lats) + 1

def test_cluster_processing():
    lats = common.get_vrp_lats()
    clusters = common.get_dbscan_clusters()

    assert len(lats) == len(clusters)