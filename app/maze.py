from flask import Blueprint, render_template, request, url_for
from .models import Token

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
    maze_size = request.form.get('size')
    return render_template('maze/partials/maze.html', size=int(maze_size))


@bp.route('/solutions', methods=['POST'])
def get_solution():
    grid_size = request.form.get('grid_size')
    population_size = request.form.get('population_size')
    generation_size = request.form.get('generation_size')
    return '<button class="solve-button">TEST</button>'