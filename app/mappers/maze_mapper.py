import networkx as nx

from app.models import Maze

brush_to_numerical = {
    'path': 0,
    'wall': -1,
    'agent': -2,
    'token-common': 1,
    'token-rare': 2,
    'token-unique': 5,
    'token-legendary': 10
}


def to_maze(values: list['str'], size: int) -> list[list[int]]:
    maze = []

    start = 0
    for _ in range(size):
        end = start + size
        row = values[start: end]
        maze.append([brush_to_numerical[value] for value in row])
        start = end

    return maze


def to_graph(maze: list[list[int]]) -> tuple[nx.Graph, int | None, list | dict]:
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

    interest_points = [node[1] for node in graph.nodes.data() if
                       node and (node[1]['value'] > 0 or node[1]['value'] == -2)]
    # find the shortest path between each interest node
    paths = {}
    for point1 in interest_points:
        for point2 in interest_points:
            if point1 == point2:
                continue

            if paths.get((point1['id'], point2['id'])) is None:
                try:
                    path = nx.shortest_path(graph, source=point1['id'], target=point2['id'])
                    paths[(point1['id'], point2['id'])] = path
                    paths[(point2['id'], point1['id'])] = path
                except nx.NetworkXNoPath and nx.NodeNotFound:
                    continue

    # construct the weighed graph
    weighted_graph = nx.Graph()
    starting_node_id = None
    for point in interest_points:
        profit = point['value'] if point['value'] > 0 else 0
        if point['value'] == -2:
            starting_node_id = point['id']
        weighted_graph.add_node(point['id'], profit=profit, row=point['row'], col=point['col'])

    for node1 in weighted_graph.nodes():
        for node2 in weighted_graph.nodes():
            node_combo = sorted([node1, node2])
            if (node_combo[0], node_combo[1]) in paths:
                path = paths[(node_combo[0], node_combo[1])]
                if set(path[1:-1]).isdisjoint(set([point['id'] for point in interest_points])):
                    weighted_graph.add_edge(node_combo[0], node_combo[1], cost=len(path) - 1)

    return weighted_graph, starting_node_id, paths
