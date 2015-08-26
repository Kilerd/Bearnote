# -*- coding: utf-8 -*-
from app import db
from datetime import datetime
from app.note import constants as NOTECONSTANTS
from app.users.models import User


class NoteID(db.DynamicDocument):
	name = db.StringField(default="noteid",required=True)
	seq = db.IntField(required=True)
	meta = {
		'collection': 'note'
	}

class NoteCate(db.Document):
	name = db.StringField(required=True)
	abbname = db.StringField(required=True)
	belong = db.ReferenceField(User)

class Note(db.DynamicDocument):
	
	noteid = db.IntField(required=True)
	title = db.StringField(max_length=60,required=True)
	subtitle = db.StringField(max_length=60)
	content = db.StringField(required=True)
	public_status = db.IntField(default=NOTECONSTANTS.PRIVATE)
	public_cate = db.ReferenceField(NoteCate)
	blog_status = db.IntField(default=NOTECONSTANTS.IS_NOT_BLOG)
	blog_cate = db.StringField()
	tag = db.ListField()
	time = db.DateTimeField(default=datetime.now(),required=True)
	belong = db.ReferenceField(User)
	meta = {  
    	'ordering': ['-time']  
    }





class Mood(db.DynamicDocument):
	content = db.StringField(max_length=120, required=True)
	time = db.DateTimeField(default=datetime.now(),required=True)
	belong = db.StringField(required=True)


