from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms import TextField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo

class LoginForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])

class RegisterForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])
	username = TextField('Username', [DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Repeat Password',validators=[
		DataRequired(),
		EqualTo('password', message='Passwords must match')
		])
	accept_tos = BooleanField('I accept the TOS', [DataRequired()])

class FindPswForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])

class ForgetPswForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])
	forgetstring = TextField('ForgetString', [DataRequired()])