from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Title of activity', validators=[DataRequired()])
    team_leader = IntegerField('Team leader', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    collaborators = StringField('List of collaborator', validators=[DataRequired()])
    is_finished = BooleanField('Is it finished?')

    submit = SubmitField('Submit')
