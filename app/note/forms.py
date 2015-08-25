# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms import StringField,PasswordField,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length,InputRequired

class NoteForm(Form):
	title = StringField(u"标题",validators=[DataRequired(),InputRequired()])
	subtitle = StringField(u"副标题")
	content = TextAreaField(u"正文",validators=[DataRequired(),InputRequired()])
	public = SelectField(u'公开状态',choices=[])
	blog = SelectField(u'推送至博客',choices=[('aim', 'AIM'), ('msn', 'MSN')])
	tag = StringField()
