from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, URL, Length
from flask_babel import _, lazy_gettext as _l
from app.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        _l('Username'),
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        _l('Password'),
        validators=[
            DataRequired()
        ]
    )
    remember_me = BooleanField(
        _l('Remember Me')
    )
    submit = SubmitField(
        _l('Sign In')
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        _l('Username'),
        validators=[
            DataRequired()
        ]
    )
    email = StringField(
        _l("Email"),
        validators=[
            Email(message="Not a valid email address."),
            DataRequired()
        ]
    )
    password = PasswordField(
        _l("Password"),
        validators=[
            DataRequired(message="Please enter a password.")
        ]
    )
    confirmPassword = PasswordField(
        _l('Repeat Password'),
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    title = SelectField(
        _l("Title"),
        validators=[
            DataRequired()
        ],
        choices=[
            ("Farmer", "farmer"),
            ("Corrupt Politician", "politician"),
            ("No-nonsense City Cop", "cop"),
            ("Professional Rocket League Player", "rocket"),
            ("Lonely Guy At A Diner", "lonely"),
            ("Pokemon Trainer", "pokemon"),
        ],
    )
    website = StringField(
        "Website",
        validators=[
            URL()
        ]
    )
    birthday = DateField("Your Birthday")
    recaptcha = RecaptchaField()
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ]
    )
    body = StringField(
        'Message',
        [
            DataRequired(),
            Length(min=4,
            message=('Your message is too short.'))
        ]
    )
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


