from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g


common_module = Blueprint('common_module',__name__)



@common_module.route('/',methods=['GET'])
def index_function():
	return render_template('common/index.html')

@common_module.route('/pricing',methods=['GET'])
def pricing_function():
	return 'Pricing Page'

@common_module.route('/feature',methods=['GET'])
def feature_function():
	return 'feature Page'

@common_module.route('/about',methods=['GET'])
def about_function():
	return 'About Page'

@common_module.route('/tos',methods=['GET'])
def tos_function():
	return 'ToS Page'