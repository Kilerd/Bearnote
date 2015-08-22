# -*- coding: utf-8 -*-
from app import db
from app.users import constants as USERCONSTANTS

class User(db.DynamicDocument):
	
	email = db.StringField(max_length=30,required=True)
	password = db.StringField(required=True)
	username = db.StringField(min_length=3,max_length=12,required=True)
	role = db.IntField(default=USERCONSTANTS.USER)
	status = db.IntField(default=USERCONSTANTS.NEW)
	description = db.StringField(max_length=160)
