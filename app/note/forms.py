# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField, URLField
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, InputRequired


class NoteForm(Form):
    title = StringField(u"标题", validators=[DataRequired(), InputRequired()])
    subtitle = StringField(u"副标题")
    content = TextAreaField(u"正文", validators=[])
    public = SelectField(u'公开状态', choices=[])
    tag = StringField()


class CommentForm(Form):
    name = StringField(u"名称", validators=[DataRequired(), InputRequired()])
    email = EmailField(u"邮箱", validators=[DataRequired(), InputRequired()])
    domain = URLField(u"个人主页")
    content = TextAreaField(
        u"内容", validators=[DataRequired(), InputRequired()])
