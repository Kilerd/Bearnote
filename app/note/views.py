# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,flash,url_for,session
from app.note.models import *
from app.users.decorators import require_login
from app.users.models import User
from app.note.forms import NoteForm
from app.note import constants as NOTECONSTANTS
from app.note.lib import getnextseq

note_module = Blueprint('note_module',__name__)


@note_module.route('/new',methods=['GET','POST'])
@require_login
def note_new_function():
	note_new_form = NoteForm()
	if note_new_form.validate_on_submit():
		Note(
			noteid=getnextseq(),
			title=note_new_form.title.data,
			subtitle=note_new_form.subtitle.data,
			content = note_new_form.content.data,
			tag = note_new_form.tag.data.split(","),
			belong = (User.objects(email=session['user']['email']).first())
			).save()
		return redirect(url_for('note_module.note_new_function'))
	return render_template('note/note_new.html',note_new_form = note_new_form)


@note_module.route('/mynote',methods=['GET'])
@require_login
def mynote_function():
	# Page Control
	note_count = Note.objects(belong=User.objects(email=session['user']['email']).first()).count()
	page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1 if note_count % NOTECONSTANTS.PER_PAGE_COUNT else note_count / NOTECONSTANTS.PER_PAGE_COUNT
	now_page = request.args.get('page',1)
	now_page = now_page if now_page >=1 or now_page <= page_count else page_count
	now_page_note = Note.objects(belong=User.objects(email=session['user']['email']).first()).skip(NOTECONSTANTS.PER_PAGE_COUNT*(now_page-1)).limit(NOTECONSTANTS.PER_PAGE_COUNT)
	return render_template('note/mynote.html',notes = now_page_note)



@note_module.route("/testid")
def getnextseqsssss():
	if NoteID.objects(name="noteid").count() == 0:
		NoteID(name="noteid",seq=0).save()

	now_seq = NoteID.objects(name="noteid").first()

	return str(now_seq.seq)