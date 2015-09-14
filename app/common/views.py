from flask import Blueprint, render_template,request,redirect,flash,url_for,session,g
from app.users.views import *
from app.users.models import Blog
from app.lib import common
from app.public.views import *
from app.common.decorators import require_base_domain
from app.common import constants as COMMONCONSTANTS
common_module = Blueprint('common_module',__name__)



@common_module.route('/',methods=['GET'])
def index_function():

    this_domain = common.get_domain()
    if this_domain in COMMONCONSTANTS.BASE_DOMAIN:
        return render_template('common/index.html')
    else:
        if Blog.objects(domain = this_domain).count() == 1:
            this_blog = Blog.objects(domain = this_domain).first()
            return member_page_function(username = this_blog.belong.username)
        else:
            return "Blog Not Found",404

@common_module.route('/pricing',methods=['GET'])
@require_base_domain
def pricing_function():
    return 'Pricing Page'

@common_module.route('/feature',methods=['GET'])
@require_base_domain
def feature_function():
    return 'feature Page'

@common_module.route('/about',methods=['GET'])
@require_base_domain
def about_function():
    return 'About Page'

@common_module.route('/tos',methods=['GET'])
@require_base_domain
def tos_function():
    return 'ToS Page'