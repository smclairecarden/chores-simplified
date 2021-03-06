from crypt import methods
from operator import methodcaller
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from myapp import db
from myapp.models import User, Chore
from myapp.users.forms import RegistrationForm, LoginForm, UpdateUserForm

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('users.user_posts')

            return redirect(next)

    return render_template('login.html',form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/account')
@login_required
def user_posts():
    username=current_user.username
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    chores = Chore.query.filter_by(author=user).order_by(Chore.done.asc()).paginate(page=page, per_page=5) 
    return render_template('user_chores.html', chores=chores, user=user)