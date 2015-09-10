# -*- coding: utf-8 -*-
from flask import g,flash,redirect,url_for,request,session,render_template
from functools import wraps


def require_bearnote(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        bearnote_url = ['http://www.bearnote.com/','https://www.bearnote.com/','http://127.0.0.1:5000/']
        if not request.url_root in bearnote_url:
            return render_template('404.html'),404
        return f(*args,**kwargs)
    return decorated_function

