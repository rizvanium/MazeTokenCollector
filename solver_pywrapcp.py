from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

'''
Solution is unfinished therefore it doesn't work
'''

def solve_max_tokens(graph, interest_points, max_distance):
    manager = pywrapcp.RoutingIndexManager(len(interest_points), 1, [len(interest_points) - 2],
                                           [len(interest_points) - 1])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        point1 = interest_points[from_node]
        point2 = interest_points[to_node]

        if point1 == 40 or point2 == 40:
            return 0

        [point1, point2] = sorted([point1, point2])

        distance = len(paths[(point1, point2)]) - 1
        return distance

    def points_callback(index):
        node = manager.IndexToNode(index)
        point = interest_points[node]
        value = graph.nodes(data=True)[point]['value']

        if value == -2 or None:
            value = 0

        return value

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,
        max_distance,
        True,
        dimension_name
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    # distance_dimension.SetGlobalSpanCostCoefficient(100)

    points_callback_index = routing.RegisterUnaryTransitCallback(points_callback)
    routing.AddDimensionWithVehicleCapacity(points_callback_index, 0, [40], True, 'Points')
    points_dimension = routing.GetDimensionOrDie('Points')

    # allow node dropping
    value_max = 10
    for node in range(0, len(interest_points) - 1):
        point = interest_points[node]
        point_value = graph.nodes(data=True)[point]['value']
        if point_value == -2 or point == 40:
            continue

        routing.AddDisjunction([manager.NodeToIndex(node)], value_max + 1)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    return routing.SolveWithParameters(search_parameters)
