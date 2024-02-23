import networkx as nx
from app.solvers.solver_ga_v2 import solve_for_max_profit


def maze_to_graph(maze):
    graph = nx.Graph()

    node_id = 0
    for i, row in enumerate(maze):
        prev_path_node = None
        for j, cell in enumerate(row):
            if cell == -1:
                prev_path_node = None
            else:
                current_node = {'id': node_id, 'value': cell, 'row': i, 'col': j}
                graph.add_node(current_node['id'], **current_node)

                # join horizontally
                if prev_path_node:
                    graph.add_edge(current_node['id'], prev_path_node['id'])

                # find out if there is node above
                node_above = next(
                    (node for node in graph.nodes(data=True) if node[1]['row'] == i - 1 and node[1]['col'] == j), None)

                # join vertically
                if i > 0 and node_above is not None:
                    graph.add_edge(current_node['id'], node_above[1]['id'])

                prev_path_node = current_node
                node_id += 1

    return graph


if __name__ == '__main__':
    maze = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, 0, -1, 0, 0, 0, 0, 0, 10, -1],
        [-1, 1, -1, 0, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, 0, 0, 0, 2, 0, 0, -1],
        [-1, 1, -1, 0, -1, -1, -1, -1, 0, -1],
        [-1, 0, -1, 0, -2, -1, 1, -1, 0, -1],
        [-1, 2, -1, -1, 0, -1, 0, 0, 0, -1],
        [-1, 0, -1, 5, 0, -1, -1, -1, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    ]

    maze_graph = maze_to_graph(maze)

    # extract only interest nodes
    interest_points = [node[1] for node in maze_graph.nodes.data() if
                       node and (node[1]['value'] > 0 or node[1]['value'] == -2)]

    # find the shortest path between each interest node
    paths = {}
    for point1 in interest_points:
        for point2 in interest_points:
            if point1 == point2:
                continue

            point_combo = sorted([point1['id'], point2['id']])
            if paths.get((point_combo[0], point_combo[1])) is None:
                try:
                    path = nx.shortest_path(maze_graph, source=point1['id'], target=point2['id'])
                    paths[(point_combo[0], point_combo[1])] = path
                except nx.NetworkXNoPath and nx.NodeNotFound:
                    continue

    weighted_graph = nx.Graph()
    id_counter = 0
    for point in interest_points:
        profit = point['value'] if point['value'] > 0 else 0
        weighted_graph.add_node(point['id'], profit=profit, row=point['row'], col=point['col'])

    for node1 in weighted_graph.nodes():
        for node2 in weighted_graph.nodes():
            node_combo = sorted([node1, node2])
            if (node_combo[0], node_combo[1]) in paths:
                path = paths[(node_combo[0], node_combo[1])]
                if set(path[1:-1]).isdisjoint(set([point['id'] for point in interest_points])):
                    weighted_graph.add_edge(node_combo[0], node_combo[1], cost=len(path) - 1)

    print(weighted_graph)

    starting_node_id = 22
    distance_limit = 45
    solve_for_max_profit(weighted_graph, starting_node_id, distance_limit)
