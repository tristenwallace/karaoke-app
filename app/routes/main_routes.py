from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/session')
def session():
    # Logic to handle session management
    return render_template('session.html')