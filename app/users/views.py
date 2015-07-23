from app.users.models import * 
from flask import Blueprint, render_template,request
from app.users.forms import LoginForm
sign_module = Blueprint('sign_module',__name__)

@sign_module.route('/signin/', methods=['GET', 'POST'])
def sign_moudle_signin():
	login = LoginForm()
	if request.method == 'GET':
		
		users = User.objects.first()

		users.update(username="aaa")
		return render_template("users/signin.htm",login=login)
	
	elif request.method == 'POST':

		return request.form['username']+" "+request.form['password']