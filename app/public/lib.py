# -*- coding: utf-8 -*-
from app.users.models import *
from app.note.models import *

def get_user(username):
	if User.objects(_username = username.lower()).count() == 1:
		return User.objects(_username = username.lower()).first()
	else:
		return 0

def get_cate(user,abbname):
    if user == 0:
        return 0
    if NoteCate.objects(abbname=abbname,belong=user).count() == 1:
        return NoteCate.objects(abbname=abbname,belong=user).first()
    else:
        return 0