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
