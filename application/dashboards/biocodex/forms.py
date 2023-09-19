from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.users.models import User


class EditForm(FlaskForm):
    nom = StringField('Username')
    prenom = StringField('Password')
    submit = SubmitField('Submit')