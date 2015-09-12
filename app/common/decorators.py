# -*- coding: utf-8 -*-
from flask import g,flash,redirect,url_for,request,session,render_template
from functools import wraps
from app.common import constants as BASECONSTANT
from app.lib.common import get_domain

def require_base_domain(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not get_domain() in BASECONSTANT.BASE_DOMAIN:
            return "404 page",404
        return f(*args,**kwargs)
    return decorated_function

