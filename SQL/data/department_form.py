from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Department email', validators=[DataRequired()])

    submit = SubmitField('Submit')
