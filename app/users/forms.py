# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo,Length,InputRequired

class LoginForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])
	password = PasswordField('Password',validators=[DataRequired(),Length(6,18),InputRequired()])


class RegisterForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])
	username = StringField('Username', validators=[DataRequired(),Length(3,12),InputRequired()])
	password = PasswordField('Password',validators=[DataRequired(),Length(6,18),InputRequired()])
	confirm_password = PasswordField('Repeat Password',validators=[
		DataRequired(),
		InputRequired(),
		EqualTo('password', message='Passwords must match')
		])
	accept_tos = BooleanField(u"我同意网站的用户手册(ToS)", [DataRequired()])


class ForgetPswForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])

class ResetPswForm(Form):
	email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])
	forgetstring = StringField('ForgetString', [DataRequired(),InputRequired()])
	password = PasswordField('New Password',validators=[DataRequired(),Length(6,18),InputRequired()])
	confirm_password = PasswordField('Repeat Password',validators=[
		DataRequired(),
		InputRequired(),
		EqualTo('password', message='Passwords must match')
		])