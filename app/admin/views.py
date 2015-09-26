from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g
from app.users.models import User
from app.note.models import Note
admin_module = Blueprint('admin_module',__name__)

@admin_module.route("/",methods=['GET'])
def index_function():
    return '123'

@admin_module.route('/user',methods=['GET'])
def user_function():
    all_user = User.objects()
    return render_template('admin/user.html',all_user=all_user)

@admin_module.route('/note',methods=['GET'])
def note_function():
    all_note = Note.objects()
    return render_template('admin/note.html',all_note=all_note)
