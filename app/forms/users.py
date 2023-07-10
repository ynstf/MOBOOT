from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# Registeration form
class RegisterForm(FlaskForm):
    name = StringField(label="name", validators=[DataRequired()])
    last_name = StringField(label="last_name", validators=[DataRequired()])
    email = StringField(label="email", validators=[DataRequired(), Email()])
    password = PasswordField(label="password", validators=[DataRequired(), Length(min=6)])
    confirm  = PasswordField(label="confirm", validators=[DataRequired(),EqualTo(fieldname='password')])
    submit = SubmitField(label="Register")

# login form
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

# shearch input in admin page
class sherch(FlaskForm):
    reserch = StringField(label="reserch", validators=[DataRequired()])