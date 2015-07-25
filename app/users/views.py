# -*- coding: utf-8 -*-
from app.users.models import * 
from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g
from app.users.forms import LoginForm,RegisterForm,ResetPswForm,ForgetPswForm
from app.users.decorators import require_login,require_not_login
from app.users.lib import UserCheck
from app.lib.mail import mail_send
import time
# init sign module
sign_module = Blueprint('sign_module',__name__)

@sign_module.route('/me',methods=['GET'])
@require_login
def me_function():
	print 'me send mail'
	#mail_send(subject = 'login',recipients = ['544372225@qq.com'],text_body = 'welcome back')
	return render_template('users/me.html')


@sign_module.route('/login', methods=['GET', 'POST'])
@require_not_login
def login_function():
	login = LoginForm()
	login_check = UserCheck()
	if request.method=='POST':
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
				print 'loginin send mail'
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
	register_check = UserCheck()
	if request.method == 'POST':
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
				# Register Email
				# mail_send(subject = 'login',recipients = [login.email.data],text_body = 'welcome back')

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
	forget_check = UserCheck()
	if request.method == 'POST':
		if forgetpsw.validate_on_submit():

			user_count = User.objects(email=forgetpsw.email.data).count()
			if user_count == 1:
				
				this_user = User.objects(
					email=forgetpsw.email.data,
					).first()
				now_time = int(time.time())
				
				if not 'forget' in this_user:

					forgetstring = forget_check.forgetstring_encrypt(
						email = forgetpsw.email.data)
					this_user.forget={
						'string': forgetstring,
						'time': int(time.time())
					}
					this_user.save()
					flash(u"已发送密码重置邮件，请前往邮箱查收。邮件一小时内有效")
					return redirect(url_for('sign_module.forgetpassword_function'))

				else:
					if now_time - int(this_user.forget['time']) > 3600:
						# Overtime
						forgetstring = forget_check.forgetstring_encrypt(
							email = forgetpsw.email.data)
						this_user.forget={
							'string': forgetstring,
							'time': int(time.time())
						}
						this_user.save()
						# send mail
						flash(u"原密码重置邮件已失效，已重新生成并发送密码重置邮件，请前往邮箱查收")
						return redirect(url_for('sign_module.forgetpassword_function'))
					elif (now_time - int(this_user.forget['time']) < 3600) and (now_time - int(this_user.forget['time']) > 60):
						#send mail
						this_user.forget['time'] = now_time
						this_user.save()
						flash(u"密码重置邮件已重新发送")
						return redirect(url_for('sign_module.forgetpassword_function'))
					elif now_time - int(this_user.forget['time']) < 60:
						flash(u"密码重置邮件已发送，请勿频繁操作（邮件发送间隔为 1分钟）")
						return redirect(url_for('sign_module.forgetpassword_function'))

			else:
				flash(u"邮箱尚未注册，或者邮箱异常")
				return redirect(url_for('sign_module.forgetpassword_function'))
		else:
			flash(u"请填写正确的邮箱")
			return redirect(url_for('sign_module.forgetpassword_function'))
	return render_template('users/forgetpassword.html',forgetpsw = forgetpsw)



@sign_module.route('/resetpassword',methods=['GET','POST'])
@require_not_login
def resetpassword_function():
	resetform = ResetPswForm()
	reset_check = UserCheck()
	if request.method == 'POST':
		if resetform.validate_on_submit():
			user_count = User.objects(email=resetform.email.data).count()
			if user_count == 1:
				this_user = User.objects(
					email=resetform.email.data,
					).first()
				if 'forget' in this_user and \
				this_user.forget['string'] == resetform.forgetstring.data and \
				(int((time.time())) - int(this_user.forget['time']) < 3600):
					this_user.password = reset_check.password_encrypt(
						email = resetform.email.data,
						password = resetform.password.data)
					this_user.forget = None
					this_user.save()
					flash(u"密码已经修改成功，去登陆吧")
					return redirect(url_for('sign_module.login_function'))
				else:
					flash(u"数据匹配失败，请核对你的信息")
					return redirect(url_for('sign_module.resetpassword_function'))
			else:
				flash(u"邮件验证失败")
				return redirect(url_for('sign_module.resetpassword_function'))
			
		else:
			flash(u"信息核对失败，密码修改失败，请重新输入")
			return redirect(url_for('sign_module.resetpassword_function'))
	return render_template('users/resetpassword.html',resetform = resetform)