# -*- coding: utf-8 -*-
from app.users.models import * 
from flask import Blueprint, render_template,request,redirect,flash,url_for
from app.users.forms import LoginForm,RegisterForm,ForgetPswForm
sign_module = Blueprint('sign_module',__name__)



@sign_module.route('/signin/', methods=['GET', 'POST'])
def signin_function():
	login = LoginForm()
	
	if request.method=='POST':
		if login.validate_on_submit():
			return "success"
		else:
			return "error"
	
	return render_template("users/signin.html",login=login)
	"""
	if request.method == 'GET':
		
		users = User.objects.first()

		users.update(username="aaa")
		return render_template("users/signin.html",login=login)
	
	elif request.method == 'POST':

		return request.form['username']+" "+request.form['password']
	"""


@sign_module.route('/register/', methods=['GET', 'POST'])
def register_function():
	register = RegisterForm()
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		if register.validate_on_submit():
			flash(u"注册成功")
			return redirect(url_for('sign_module.signin_function'))
		else:
			pass
	return render_template("users/register.html",register=register)


@sign_module.route('/forgetpassword',methods=['GET','POST'])
def forgetpassword_function():
	forgetpsw = ForgetPswForm()
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		if forgetpassword.validate_on_submit():
			flash(u"密码修改成功")
			return redirect(url_for('sign_module.signin_function'))
		else:
			pass
	return render_template('users/forgetpassword.html',forgetpsw = forgetpsw)