from ortools.sat.python import cp_model

'''
Unimplemented
'''


def solve_max_profit(graph, max_distance):
    model = cp_model.CpModel()

    node_count = len(graph.nodes)
    max_steps = node_count - 1

    path = [model.NewIntVar(0, node_count - 1, f'node_{i}') for i in range(max_steps)]
    steps = [model.NewIntVar(0, max_distance, f'step_weight_{i}') for i in range(max_steps - 1)]
    total_distance = model.NewIntVar(0, max_distance, 'total_distance')

    model.Add(sum(steps[i] for i in range(max_steps - 1)) <= max_distance)

    total_profit = model.NewIntVar(0, sum(node['profit'] for node in graph.nodes(data=True)), 'total_profit')

    model.Add(total_profit == sum())
    model.Maximize(total_profit)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    return status, solver
