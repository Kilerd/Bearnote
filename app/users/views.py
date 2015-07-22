from flask import Blueprint, render_template,request

sign_module = Blueprint('sign_module',__name__)

@sign_module.route('/signin/', methods=['GET', 'POST'])
def sign_moudle_signin():
	if request.method == 'GET':
		return render_template("users/signin.htm")
	elif request.method == 'POST':

		return request.form['username']+" "+request.form['password']