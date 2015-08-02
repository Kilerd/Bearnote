# -*- coding: utf-8 -*-
from app import db
from datetime import datetime
from app.users.models import User
from app.note import constants as NOTECONSTANTS

class Note(db.DynamicDocument):
	
	title = db.StringField(max_length=60,required=True)
	subtitle = db.StringField(max_length=60)
	content = db.StringField(required=True)
	public_status = db.IntField(default=NOTECONSTANTS.PRIVATE)
	public_cate = db.StringField()
	blog_status = db.IntField(default=NOTECONSTANTS.IS_NOT_BLOG)
	blog_cate = db.StringField()
	tag = db.ListField()
	belong = db.ReferenceField(User)




class Mood(db.DynamicDocument):
	content = db.StringField(max_length=120, required=True)
	time = db.DateTimeField(default=datetime.now(),required=True)
	belong = db.StringField(required=True)