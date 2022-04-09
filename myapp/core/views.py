# core/views.py 
from flask import render_template, request, Blueprint
from myapp.models import Chore, User


core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    chores = Chore.query.order_by(Chore.done.asc()).paginate(page=page, per_page=5)

    return render_template('index.html', chores=chores)


@core.route('/info')
def info():
    return render_template('info.html')