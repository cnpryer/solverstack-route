"""
module for running test cases for model scoring.

TODO: use logging to define case logging
"""
from tests.cases import DATA
from app.vrp_model import model, distance
from app.vrp_model.scoring import input_scoring, output_scoring


def get_dlats_from_case(case: dict):
    """pull list of latitudes from test case"""
    dlats = [geo[0] for geo in case["destinations"]]

    return dlats


def get_dlons_from_case(case: dict):
    """pull list of latitudes from test case"""
    dlons = [geo[1] for geo in case["destinations"]]

    return dlons


def create_matrix_from_case(case: dict):
    """generate distance matrix input using test case"""
    matrix = distance.create_matrix(
        (case["origin"][0], case["origin"][1]),
        get_dlats_from_case(case),
        get_dlons_from_case(case),
    )

    return matrix


def run_case(case: dict):
    """run test case"""
    matrix = create_matrix_from_case(case)

    bndl = model.VrpBasicBundle(
        distance_matrix=matrix,
        demand_quantities=case["demand"],
        max_vehicle_capacity_units=max(case["vehicles"]),
        max_search_seconds=30,
    )

    solution = bndl.run().get_solution()

    return solution


def score_inputs(case: dict):
    """score inputs defined in test case"""
    matrix = create_matrix_from_case(case)
    dests_score = input_scoring.get_stop_distance_factor(matrix)
    origin_score = input_scoring.get_origin_position_factor(matrix)

    print(f"{case['id']} | origin score: {origin_score}")
    print(f"{case['id']} | dests score: {dests_score}")


def score_outputs(case: dict, solution: dict):
    """score outputs from model"""
    matrix = create_matrix_from_case(case)

    load_factor = output_scoring.get_load_factor(
        vehicles=solution["id"],  # TODO: not clear this is a vehicle id
        demand=case["demand"],
    )
    aggregation_score = output_scoring.get_aggregation(
        vehicles=solution["id"], demand=case["demand"]
    )
    stop_dist_score = output_scoring.get_stop_distance_factor(
        vehicles=solution["id"], stops=solution["stops"], matrix=matrix
    )
    route_dist_score = output_scoring.get_route_distance_factor(
        vehicles=solution["id"], stops=solution["stops"], matrix=matrix
    )

    print(f"{case['id']} | load factor: {load_factor}")
    print(f"{case['id']} | aggregation score: {aggregation_score}")
    print(f"{case['id']} | stop distance score: {stop_dist_score}")
    print(f"{case['id']} | route distance score: {route_dist_score}")


def main():
    """run all test cases"""
    for case in DATA:
        print(f"{case['id']} :: description: {case['desc']}")

        score_inputs(case)
        solution = run_case(case)
        score_outputs(case, solution)


if __name__ == "__main__":
    main()
