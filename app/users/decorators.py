# -*- coding: utf-8 -*-
from flask import g,flash,redirect,url_for,request,session
from functools import wraps


def require_signin(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		if not 'user' in session:
			flash(u"请先登录，亲")
			return redirect(url_for('sign_module.signin_function',next=request.path))
		return f(*args,**kwargs)
	return decorated_function


def require_not_signin(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		if 'user' in session:
			flash(u"已经登陆了喔，亲")
			return redirect(url_for('sign_module.me_function'))
		return f(*args,**kwargs)
	return decorated_function

	