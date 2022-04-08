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
        chore = Chore(title=form.chore.data, description=form.description.data,  completed_by=form.completed_by.data,done=form.done.data, user_id=current_user.id)
        db.session.add(chore)
        db.session.commit()
        flash('Chore Created')
        print('Chore was created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

```python
# Make sure the blog_post_id is an integer!

@chores.route('/<int:chore_id>')
def chore(chore_id):
    chore = BlogPost.query.get_or_404(blog_post_id) 
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)
```