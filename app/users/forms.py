from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Accepts a username and a room."""
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Login')
