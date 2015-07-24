# -*- coding: utf-8 -*-
from app.users.models import * 
from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g
from app.users.forms import LoginForm,RegisterForm,ForgetPswForm
from app.users.decorators import require_signin,require_not_signin
# init sign module
sign_module = Blueprint('sign_module',__name__)

@sign_module.route('/me',methods=['GET'])
@require_signin
def me_function():
	return render_template('users/me.html')


@sign_module.route('/signin', methods=['GET', 'POST'])
@require_not_signin
def signin_function():
	login = LoginForm()

	if request.method=='GET':
	#GET
		pass
	elif request.method=='POST':
	#POST
		if login.validate_on_submit():
			# Count the User of input information
			user_count = User.objects(email=login.email.data,password=login.password.data).count()
			
			if user_count == 1:
				# Login successful
				
				# Add Session
				session['user'] = User.objects(email=login.email.data,password=login.password.data).first()

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
				return redirect(url_for('sign_module.signin_function'))
		else:
			flash(u"数据提交失败，请检查输入内容")
			return redirect(url_for('sign_module.signin_function'))

	return render_template("users/signin.html",login=login)


@sign_module.route('/register', methods=['GET', 'POST'])
@require_not_signin
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
@require_not_signin
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