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
    brush = request.form.get('brush')

    return render_template(
        'maze/partials/cell.html',
        brush=brush
    )


@bp.route('/maze', methods=['PUT'])
def update_maze():
    maze_size = request.form.get('size')
    return render_template('maze/partials/maze.html', size=int(maze_size))
