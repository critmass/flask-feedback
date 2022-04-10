from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
