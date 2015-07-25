# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class LoginForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired(),Length(6,18)])


class RegisterForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])
	username = StringField('Username', validators=[DataRequired(),Length(3,12)])
	password = PasswordField('Password',validators=[DataRequired(),Length(6,18)])
	confirm_password = PasswordField('Repeat Password',validators=[
		DataRequired(),
		EqualTo('password', message='Passwords must match')
		])
	accept_tos = BooleanField('I accept the TOS', [DataRequired()])


class ForgetPswForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])

class ResetPswForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email()])
	forgetstring = StringField('ForgetString', [DataRequired()])
	password = PasswordField('New Password',validators=[DataRequired(),Length(6,18)])
	confirm_password = PasswordField('Repeat Password',validators=[
		DataRequired(),
		EqualTo('password', message='Passwords must match')
		])