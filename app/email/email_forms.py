from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class SendEmailForm(FlaskForm):
    body = TextAreaField("Enter your message", validators=[DataRequired()])
    submit = SubmitField("Send")
