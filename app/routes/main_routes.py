from flask import Blueprint, render_template
from app.models import ConfTemplate

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    templates = ConfTemplate.query.all()
    return render_template('index.html', templates=templates)

