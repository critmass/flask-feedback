from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(max=20)]
    )
    first_name = StringField(
        'First Name',
        validators=[DataRequired(), Length(max=30)]
    )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired(), Length(max=30)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Length(max=50)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6)]
    )


class LoginForm(FlaskForm):

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(max=20)]
    )
    password = PasswordField('Password', validators=[Length(min=6)])

class FeedbackForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=100)]
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

