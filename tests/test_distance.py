from . import common


def test_matrix_processing():
    matrix = common.get_matrix_basic()
    demand_lats = common.get_vrp_lats_basic()

    assert len(matrix) == len(demand_lats) + 1


def test_cluster_processing():
    lats = common.get_vrp_lats_basic()
    clusters = common.get_dbscan_clusters_basic()

    assert len(lats) == len(clusters)
