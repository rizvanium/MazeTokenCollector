import json

from flask import Blueprint, render_template, request, jsonify

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

    for index, individual in enumerate(hof):
        print(
            f'{index + 1}.\t{individual} points: {individual.fitness.values[0]}, distance: {individual.fitness.values[1]}')
    # concat into path for drawing
    solutions = []
    for individual in hof:
        if individual.fitness.values[0] <= 0:
            continue
        solution_path = [individual[0]]
        for i in range(len(individual) - 1):
            point1, point2 = individual[i], individual[i + 1]
            path_between = paths[(point1, point2)]
            if point1 != path_between[0]:
                path_between = list(reversed(path_between))
            solution_path += path_between[1:]
        solutions += [
            {
                'path': solution_path,
                'total_points': individual.fitness.values[0],
                'steps_taken': individual.fitness.values[1],
            }
        ]

    if not success:
        return '<button class="solve-button">FAILURE</button>'

    return render_template(
        'maze/partials/maze.html',
        size=grid_size,
        solution_path=solutions[0]['path'],
        cells=maze_cells,
        solutions=solutions
    )


@bp.route('/solutions', methods=['PUT'])
def select_path():
    grid_size = int(request.form.get('grid_size'))
    maze_cells = [v for k, v in request.form.items() if k.isnumeric()]

    solution_path = request.form.get('solution_path')
    solution_path_json = json.dumps(solution_path)
    solution_path = json.loads(json.loads(solution_path_json))

    solutions = request.form.get('solutions')
    solutions_json = solutions.replace("'", '"')
    solutions = json.loads(solutions_json)

    return render_template(
        template_name_or_list='maze/partials/selected_solutions.html',
        size=grid_size,
        solution_path=solution_path,
        cells=maze_cells,
        solutions=solutions,
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
