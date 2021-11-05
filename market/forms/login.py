from flask_wtf import FlaskForm
from jsonschema import ValidationError
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from market.models.user import User


class LoginForm(FlaskForm):
    email_address = StringField(label='email', validators=[DataRequired()])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='sign in')

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if not email:
            raise ValidationError('Email address already exist.')
