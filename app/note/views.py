# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,flash,url_for,session
from app.note.models import *
from app.users.decorators import require_login
from app.users.models import User
from app.note.forms import NoteForm

note_module = Blueprint('note_module',__name__)


@note_module.route('/new',methods=['GET','POST'])
@require_login
def note_new_function():
	note_new_form = NoteForm()
	if note_new_form.validate_on_submit():
		Note(title=note_new_form.title.data,
			subtitle=note_new_form.subtitle.data,
			content = note_new_form.content.data,
			tag = note_new_form.tag.data.split(","),
			belong = User.objects(email=session['user']['email']).first()
			).save()
	return render_template('note/note_new.html',note_new_form = note_new_form)