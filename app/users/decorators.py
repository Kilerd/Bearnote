# -*- coding: utf-8 -*-
from flask import flash, redirect, url_for, request, session
from functools import wraps


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash(u"请先登录，亲")
            return redirect(url_for('sign_module.login_function', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def require_not_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            flash(u"已经登陆了喔，亲")
            return redirect(url_for('sign_module.me_function'))
        return f(*args, **kwargs)
    return decorated_function
