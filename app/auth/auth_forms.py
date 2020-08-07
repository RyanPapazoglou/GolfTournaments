from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import Users


def ValidateEmailExits(form, field):
    user = Users.query.filter_by(email=field.data).first()
    if user is None:
        raise ValidationError("No account exists with the provided email address.")


def ValidateTeamname(form, field):
    user = Users.query.filter_by(team_name=field.data).first()
    if user is not None:
        raise ValidationError("Please use a different team name.")


def ValidateEmail(form, field):
    user = Users.query.filter_by(email=field.data).first()
    if user is not None:
        raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(), ValidateEmail])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    team_name = StringField("Team name", validators=[DataRequired(), ValidateTeamname])
    submit = SubmitField("Register")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), ValidateEmailExits]
    )
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Password Reset")
