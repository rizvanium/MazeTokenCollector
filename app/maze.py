from flask import Blueprint, render_template, url_for

bp = Blueprint('maze', __name__)


@bp.route('/')
def index():

    return render_template('maze/index.html')
