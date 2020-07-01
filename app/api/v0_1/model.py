"""ortools model via pyords bundle concept"""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import numpy as np


class VrpBasicBundle:

    def __init__(self, matrix:list, demand:list, max_vehicle_capacity_units:int,
        max_search_seconds:int=5):
        """
        high level implementation of an ortools capacitated vehicle routing model.

        :matrix:          [[dist0, dist1, dist2, ...], [...] ...] distance matrix of origin
                          at node 0 and demand nodes at 1 -> len(matrix) - 1.
        :demand:          [int, int, ... len(demand nodes) - 1]
        :max_vehicle_capacity_units:      int for vehicle capacity constraint (in demand units)
        :max_search_seconds:      int for seconds allowance for solver
        """
        self.matrix = matrix
        self.demand = demand
        self.max_vehicle_cap = max_vehicle_capacity_units
        self.max_search_seconds = max_search_seconds

        self.vehicles = self.create_vehicles()
        self.ortools()

        return None

    def create_vehicles(self):
        """
        assumes origin is position 0 in self.matrix and
        defines a vehicle of max_cap for each destination.
        """
        return [self.max_vehicle_cap for i in range(len(self.matrix[1:]))] 
        
    def create_manager(self):
        return pywrapcp.RoutingIndexManager(len(self.matrix), len(self.vehicles), 0)

    def matrix_callback(self, i:int, j:int):
        """index of from (i) and to (j)"""
        node_i = self.manager.IndexToNode(i)
        node_j = self.manager.IndexToNode(j)

        return self.matrix[node_i][node_j]

    def demand_callback(self, i:int):
        """capacity constraint"""
        node = self.manager.IndexToNode(i)

        return self.demand[node]

    def create_model(self):
        model = pywrapcp.RoutingModel(self.manager)

        # distance constraint setup
        model.SetArcCostEvaluatorOfAllVehicles(
            model.RegisterTransitCallback(self.matrix_callback)
        )

        # demand constraint setup
        model.AddDimensionWithVehicleCapacity(
            # function which return the load at each location (cf. cvrp.py example)
            model.RegisterUnaryTransitCallback(self.demand_callback),
            0, # null capacity slack
            np.array([cap for cap in self.vehicles]), # vehicle maximum capacity
            True, # start cumul to zero
            'Capacity'
        )

        return model

    def create_search_params(self, max_seconds:int=5):
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = \
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.time_limit.seconds = max_seconds
        
        return search_parameters

    def get_solution(self):
        total_distance = 0
        total_load = 0

        # positions in matrix (demand)
        solution = np.zeros(len(self.demand) - 1)
        
        # original solution building
        for vehicle in range(len(self.vehicles)):
            i = self.model.Start(vehicle)
            info = {'vehicle': vehicle, 'stops': list(), 'stop_distances': [0],
                    'stop_loads': list()}

            while not self.model.IsEnd(i):
                node = self.manager.IndexToNode(i)

                if node != 0:
                    solution[node - 1] = vehicle

                info['stops'].append(node)
                info['stop_loads'].append(self.demand[node])

                previous_i = int(i)
                i = self.assignment.Value(self.model.NextVar(i))
                info['stop_distances'].append(self.model.GetArcCostForVehicle(previous_i, i, vehicle))

            # add return to depot to align with solution data
            info['stops'].append(0)
            info['stop_loads'].append(0)
            #solution.append(info)
        
        # NOTE: returning vehicle assignments only
        return list(solution)

    def ortools(self):
        """init of ortools modeling"""
        self.manager = self.create_manager()
        self.model = self.create_model()

        return self

    def run(self, max_search_seconds:int=30):
        search = self.create_search_params(max_search_seconds)
        self.assignment = self.model.SolveWithParameters(search)

        return self

def create_vehicles(matrix:list, demand:list, clusters:list, max_vehicle_capacity_units:int=26):
    """
    solve by cluster and return assigned list of vehicles
    
    :matrix:      list of lists for all-to-all distances (includes origin)
    :demand:      list of demand (includes origin zero'd)
    :clusters:    numpy array of cluster output. length is matrix|demand - 1

    returns vehicles:list
    """
    vehicles = np.zeros(len(demand) - 1)
    matrix = np.array(matrix)
    demand = np.array(demand)

    for c in np.unique(clusters):

        # align with matrix, demand
        is_cluster = np.where(clusters == c)[0]
        is_cluster = is_cluster + 1
        is_cluster = np.insert(is_cluster, 0, 0)

        bndl = VrpBasicBundle(
            matrix=matrix[is_cluster],
            demand=demand[is_cluster],
            max_vehicle_capacity_units=int(max_vehicle_capacity_units)
        )
        
        # list of vehcles # NOTE: will change
        solution = bndl.run().get_solution()

        # assign
        is_cluster = is_cluster[is_cluster != 0] - 1
        vehicles[is_cluster] = solution

    return vehicles