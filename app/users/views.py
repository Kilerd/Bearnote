from app.users.models import * 
from flask import Blueprint, render_template,request
from app.users.forms import LoginForm,RegisterForm
sign_module = Blueprint('sign_module',__name__)

@sign_module.route('/signin/', methods=['GET', 'POST'])
def sign_moudle_signin():
	login = LoginForm()
	if login.validate_on_submit():
		return "success"
	return render_template("users/signin.html",login=login)
	"""
	if request.method == 'GET':
		
		users = User.objects.first()

		users.update(username="aaa")
		return render_template("users/signin.html",login=login)
	
	elif request.method == 'POST':

		return request.form['username']+" "+request.form['password']
	"""
@sign_module.route('/register/', methods=['GET', 'POST'])
def register_function():
	register = RegisterForm()
	return render_template("users/register.html",register=register)