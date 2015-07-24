# -*- coding: utf-8 -*-
from app.users.models import * 
from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g
from app.users.forms import LoginForm,RegisterForm,ForgetPswForm
from app.users.decorators import require_login,require_not_login
from app.users.lib import PasswordCheck
# init sign module
sign_module = Blueprint('sign_module',__name__)

@sign_module.route('/me',methods=['GET'])
@require_login
def me_function():
	return render_template('users/me.html')


@sign_module.route('/login', methods=['GET', 'POST'])
@require_not_login
def login_function():
	login = LoginForm()
	login_check = PasswordCheck()
	if request.method=='GET':
	#GET
		pass
	elif request.method=='POST':
	#POST
		if login.validate_on_submit():
			# Count the User of input information
			user_count = User.objects(
				email = login.email.data,
				password = login_check.password_encrypt(
					email = login.email.data,
					password = login.password.data)
				).count()
			
			if user_count == 1:
				# Login successful
				
				# Add Session
				session['user'] = User.objects(
					email=login.email.data,
					password=login.password.data
					).first()

				next_page = request.args.get('next', '')
				if next_page == '':
					# Redirect to /me
					flash(u"欢迎回来，亲。")
					return redirect(url_for('sign_module.me_function'))
				else:
					# Redirect to next page
					return redirect(next_page)
			else:
				flash(u"用户名不存在或密码错误")
				return redirect(url_for('sign_module.login_function'))
		else:
			flash(u"数据提交失败，请检查输入内容")
			return redirect(url_for('sign_module.login_function'))

	return render_template('users/login.html',login=login)


@sign_module.route('/register', methods=['GET', 'POST'])
@require_not_login
def register_function():
	register = RegisterForm()
	register_check = PasswordCheck()
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		if register.validate_on_submit():
			# Count the User of input information
			user_count = User.objects(email=register.email.data).count()
			if user_count == 0:
				# 注销入库
				User(
					email = register.email.data,
					username = register.username.data,
					password = register_check.password_encrypt(
						email = register.email.data,
						password = register.password.data),
					).save()
				flash(u"注册成功")
				return redirect(url_for('sign_module.login_function'))
			else:
				flash(u"邮箱已经被使用，请尝试找回密码")
				return redirect(url_for('sign_module.register_function'))
		else:
			flash(u"填写的内容不完善，请重试")
			return redirect(url_for('sign_module.register_function'))
	return render_template("users/register.html",register=register)


@sign_module.route('/logout',methods=['GET'])
def logout_function():
	if 'user' in session:
		session.pop('user')
	return redirect('/')

@sign_module.route('/forgetpassword',methods=['GET','POST'])
@require_not_login
def forgetpassword_function():
	forgetpsw = ForgetPswForm()
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		if forgetpassword.validate_on_submit():
			flash(u"密码修改成功")
			return redirect(url_for('sign_module.login_function'))
		else:
			pass
	return render_template('users/forgetpassword.html',forgetpsw = forgetpsw)