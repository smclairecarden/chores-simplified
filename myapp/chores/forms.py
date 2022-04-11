from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class ChoreForm(FlaskForm):
    chore = StringField('Chore', validators=[DataRequired()])
    description = StringField('Description')
    completed_by = StringField('Completed_By')
    done = BooleanField('Done')
    submit = SubmitField('Post')
    