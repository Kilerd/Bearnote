# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms import StringField,PasswordField,BooleanField,HiddenField
from wtforms.validators import DataRequired,Email,EqualTo,Length,InputRequired

class LoginForm(Form):
    email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(6,18),InputRequired()])


class RegisterForm(Form):
    email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])
    username = StringField('Username', validators=[DataRequired(),Length(3,12),InputRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(6,18),InputRequired()])
    confirm_password = PasswordField('Repeat Password',validators=[
        DataRequired(),
        InputRequired(),
        EqualTo('password', message='Passwords must match')
        ])
    accept_tos = BooleanField(u"我同意网站的用户手册(ToS)", [DataRequired()])


class ForgetPswForm(Form):
    email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])

class ResetPswForm(Form):
    email = EmailField('Email',validators=[DataRequired(),Email(),InputRequired()])
    forgetstring = StringField('ForgetString', [DataRequired(),InputRequired()])
    password = PasswordField('New Password',validators=[DataRequired(),Length(6,18),InputRequired()])
    confirm_password = PasswordField('Repeat Password',validators=[
        DataRequired(),
        InputRequired(),
        EqualTo('password', message='Passwords must match')
        ])




# Form For Setting

class SettingAccountForm(Form):
    description = StringField(u'个人介绍',validators=[Length(0,160)])

class SettingResetPasswordForm(Form):
    beforepassword = PasswordField(u'原密码',validators=[DataRequired(),Length(6,18),InputRequired()])
    newpassword = PasswordField(u'新密码',validators=[DataRequired(),Length(6,18),InputRequired()])
    confirm_newpassword = PasswordField(u'重复新密码',validators=[
        DataRequired(),
        InputRequired(),
        EqualTo('newpassword', message='Passwords must match')
        ])



class PublicSettingAddCateForm(Form):
    name = StringField(u"分类名称",validators=[DataRequired(),Length(1,10),InputRequired()])
    abbname = StringField(u"分类缩略名",validators=[DataRequired(),Length(1,16),InputRequired()])


class PublicSettingDeleteCateForm(Form):
    hideabbname = HiddenField()
    name = StringField(u"分类名称",validators=[DataRequired(),Length(1,10),InputRequired()])
    abbname = StringField(u"分类缩略名",validators=[DataRequired(),Length(1,16),InputRequired()])
