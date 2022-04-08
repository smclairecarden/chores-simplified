from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import Chore
from myapp.chores.forms import ChoreForm

chores = Blueprint('chores', __name__)

@chores.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = ChoreForm()
    if form.validate_on_submit():
        chore = Chore(chore=form.chore.data, description=form.description.data, completed_by=form.completed_by.data, done=form.done.data, user_id=current_user.id)
        db.session.add(chore)
        db.session.commit()
        flash('Chore Created')
        print('Chore was created')
        return redirect(url_for('core.index'))
    return render_template('create_chore.html', form=form)

@chores.route('/<int:chore_id>')
def chore(chore_id):
    chore = Chore.query.get_or_404(chore_id) 
    return render_template('chore.html', title=chore.chore, date=chore.date, post=chore)

@chores.route('/<int:chore_id>/update',methods=['GET','POST'])
@login_required
def update(chore_id):
    chore = Chore.query.get_or_404(chore_id)

    if chore.author != current_user:
        abort(403)

    form = ChoreForm()

    if form.validate_on_submit():
        chore.chore = form.chore.data
        chore.description = form.description.data
        chore.completed_by = form.completed_by.data
        chore.done = form.done.data
        db.session.commit()
        flash('Chore Updated')
        return redirect(url_for('chores.chore', chore_id=chore.id))

    elif request.method == 'GET':
        form.chore.data = chore.chore
        form.description.data = chore.description
        form.completed_by.data = chore.completed_by
        form.done.data = chore.done

    return render_template('create_chore.html',title='Updating',form=form)

@chores.route('/<int:chore_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(chore_id):

    chore = Chore.query.get_or_404(chore_id)
    if chore.author != current_user:
        abort(403)

    db.session.delete(chore)
    db.session.commit()
    flash('Chore Deleted')
    return redirect(url_for('core.index'))