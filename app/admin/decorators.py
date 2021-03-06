# -*- coding: utf-8 -*-
from flask import *
from functools import wraps
from app.users import constants as USERCONSTANT


def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user']['role'] != USERCONSTANT.ADMIN:
            return '404', 404
        return f(*args, **kwargs)
    return decorated_function
