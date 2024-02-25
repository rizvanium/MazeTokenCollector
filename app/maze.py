from flask import Blueprint, render_template, request

from .solvers import solver_ga_v2
from .mappers import maze_mapper
from .models import Maze

bp = Blueprint('maze', __name__)


@bp.route('/')
def index():
    return render_template('maze/index.html')


@bp.route('/select-brush', methods=['POST'])
def select_item():
    brush = request.form.get('brush')
    return render_template(
        'maze/partials/selected_brush.html',
        selected_brush=brush
    )


@bp.route('/maze/cell', methods=['PUT'])
def update_maze_cell():
    brush = request.form.get('brush')
    prev_brush = request.form.get('prev_brush')
    idx = request.form.get('index')
    points = int(request.form.get('points'))

    points_to_add = brushes_to_points[brush]
    points_to_subtract = brushes_to_points[prev_brush]

    return render_template(
        'maze/partials/cell.html',
        brush=brush,
        index=idx,
        points=points + points_to_add - points_to_subtract
    )


@bp.route('/maze', methods=['PUT'])
def update_maze():
    maze_size = request.form.get('grid_size')
    return render_template('maze/partials/maze.html', size=int(maze_size), solution_path={})


@bp.route('/solutions', methods=['POST'])
def get_solution():
    grid_size = int(request.form.get('grid_size'))
    population_size = int(request.form.get('population_size'))
    generation_size = int(request.form.get('generation_size'))
    step_count = int(request.form.get('step_count'))

    maze_cells = [v for k, v in request.form.items() if k.isnumeric()]

    maze = maze_mapper.to_maze(values=maze_cells, size=grid_size)

    weighted_graph, starting_node_id, paths = maze_mapper.to_graph(maze=maze)

    hof, success = solver_ga_v2.solve_for_max_profit(
        graph=weighted_graph,
        starting_node_id=starting_node_id,
        distance_limit=step_count,
        population_size=population_size,
        generation_size=generation_size
    )

    best_solution = hof[0]

    # concat into path for drawing
    complete_solution_path = {starting_node_id: 1}
    for i in range(len(best_solution) - 1):
        point1, point2 = best_solution[i], best_solution[i + 1]
        path_between = paths[(point1, point2)]
        if point1 != path_between[0]:
            path_between = path_between[::-1]
        removed_first_last = {point: i + 1 for point in path_between[1:]}
        complete_solution_path = complete_solution_path | removed_first_last

    if not success:
        return '<button class="solve-button">FAILURE</button>'

    for index, individual in enumerate(hof):
        print(
            f'{index + 1}.\t{individual} points: {individual.fitness.values[0]}, distance: {individual.fitness.values[1]}')

    return render_template(
        'maze/partials/maze.html',
        size=grid_size,
        solution_path=complete_solution_path,
        cells=maze_cells
    )


brushes_to_points = {
    'path': 0,
    'wall': 0,
    'agent': 0,
    'token-common': 1,
    'token-rare': 2,
    'token-unique': 5,
    'token-legendary': 10
}
