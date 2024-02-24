from flask import Blueprint, render_template, request, url_for

from .solvers import solver_ga_v2
from .models import Token
from .mappers import maze_mapper

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
    return render_template(
        'maze/partials/cell.html',
        brush=request.form.get('brush'),
        index=request.form.get('index'),
    )


@bp.route('/maze', methods=['PUT'])
def update_maze():
    maze_size = request.form.get('grid_size')
    return render_template('maze/partials/maze.html', size=int(maze_size))


@bp.route('/solutions', methods=['POST'])
def get_solution():
    grid_size = request.form.get('grid_size')
    population_size = request.form.get('population_size')
    generation_size = request.form.get('generation_size')

    maze, paths = maze_mapper.to_maze(values=[v for k, v in request.form.items() if k.isnumeric()], size=int(grid_size))
    graph, starting_node_id = maze_mapper.to_graph(maze=maze)
    hof, success = solver_ga_v2.solve_for_max_profit(graph=graph, starting_node_id=starting_node_id, distance_limit=50)

    if success:
        for index, individual in enumerate(hof):
            print(
                f'{index + 1}.\t{individual} points: {individual.fitness.values[0]}, distance: {individual.fitness.values[1]}')
        return '<button class="solve-button">SUCCESS</button>'

    return '<button class="solve-button">FAILURE</button>'
