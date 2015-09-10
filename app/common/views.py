from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g
from app.users.views import *
from app.lib import common
from app.public.views import *
common_module = Blueprint('common_module',__name__)



@common_module.route('/',methods=['GET'])
def index_function():
    this_domain = common.get_domain()
    base_domain = ['www.baernote.com','bearnote.com','127.0.0.1:5000','121.42.201.203']
    if this_domain in base_domain:
        return render_template('common/index.html')
    else:

        return member_page_function(username = 'Kilerd')

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