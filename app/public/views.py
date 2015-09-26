# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,flash,url_for,session
from app.users.models import *
public_module = Blueprint('public_module',__name__)


@public_module.route('/member/<string:username>',methods=['GET'])
def member_page_function(username = "admin"):
    if User.objects(_username = username.lower()).count():
        this_user = User.objects(_username=username.lower()).first()

        return this_user.username
    else:
        return 'Member not found'