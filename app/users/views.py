# -*- coding: utf-8 -*-

from flask import *
from app.users.forms import *
from app.users.models import *
from app.users.decorators import require_login, require_not_login
from app.users.lib import UserCheck
from app.lib.mail import mail_send
from app.lib import common
from app.note.models import NoteCate, Note
from app.note import constants as NOTECONSTANTS
from app.common.decorators import *
import time

# init sign module
sign_module = Blueprint('sign_module', __name__)


@sign_module.route('/me', methods=['GET'])
@require_base_domain
@require_login
def me_function():
    return redirect(url_for('note_module.mynote_function'))

    return render_template('users/me.html')


@sign_module.route('/login', methods=['GET', 'POST'])
@require_base_domain
@require_not_login
def login_function():
    login = LoginForm()
    login_check = UserCheck()
    if request.method == 'POST':
        # POST
        if login.validate_on_submit():
            # Count the User of input information
            user_count = User.objects(
                email=login.email.data.lower(),
                password=login_check.password_encrypt(
                    email=login.email.data.lower(),
                    password=login.password.data)
            ).count()

            if user_count == 1:
                # Login successful

                # Add Session
                this_user = User.objects(
                    email=login.email.data,
                    ).first()
                session.permanent = True
                session['user'] = {
                    "username": this_user.username,
                    "email": this_user.email,
                    "email_md5": common.md5_encrypt(login.email.data),
                    "status": this_user.status,
                    "role": this_user.role,
                    "description": this_user.description
                }
                next_page = request.args.get('next', '')
                if next_page == '':
                    # Redirect to /me
                    flash(u"欢迎回来，亲。")
                    return redirect(url_for('sign_module.me_function'))
                else:
                    # Redirect to next page
                    return redirect(next_page)
            else:
                flash(u"用户名不存在或密码错误")
                return redirect(url_for('sign_module.login_function'))
        else:
            flash(u"数据提交失败，请检查输入内容")
            return redirect(url_for('sign_module.login_function'))

    return render_template('users/login.html', login=login)


@sign_module.route('/register', methods=['GET', 'POST'])
@require_base_domain
@require_not_login
def register_function():
    register = RegisterForm()
    register_check = UserCheck()
    if request.method == 'POST':
        if register.validate_on_submit():
            # Count the User of input information
            user_count = User.objects(email=register.email.data.lower()).count()
            if user_count == 0:
                print register.username.data.lower()
                if User.objects(_username=register.username.data.lower()).count() == 0:
                    # 注销入库
                    User(
                        email=register.email.data.lower(),
                        username=register.username.data,
                        password=register_check.password_encrypt(
                            email=register.email.data.lower(),
                            password=register.password.data),
                        _username=register.username.data.lower()
                        ).save()
                    # Register Email
                    mail_send(subject='恭喜你，小熊笔记账号注册成功！', recipients=[register.email.data.lower()], html_body=render_template('mail/user_register.html', user={"name": register.username.data, "email": register.email.data.lower()}))

                    flash(u"注册成功，请登录吧，亲")
                    return redirect(url_for('sign_module.login_function'))
                else:
                    flash(u"用户名已经被使用，请更换")
                    return redirect(url_for('sign_module.register_function'))

            else:
                flash(u"邮箱已经被使用，请尝试找回密码")
                return redirect(url_for('sign_module.register_function'))
        else:
            flash(u"填写的内容不完善，请重试")
            return redirect(url_for('sign_module.register_function'))
    return render_template("users/register.html", register=register)


@sign_module.route('/logout', methods=['GET'])
@require_base_domain
def logout_function():
    if 'user' in session:
        session.pop('user')
    return redirect('/')


@sign_module.route('/forgetpassword', methods=['GET', 'POST'])
@require_base_domain
@require_not_login
def forgetpassword_function():
    forgetpsw = ForgetPswForm()
    forget_check = UserCheck()
    if request.method == 'POST':
        if forgetpsw.validate_on_submit():

            user_count = User.objects(email=forgetpsw.email.data.lower()).count()
            if user_count == 1:

                this_user = User.objects(
                    email=forgetpsw.email.data.lower(),
                    ).first()
                now_time = int(time.time())

                if 'forget' not in this_user:

                    forgetstring = forget_check.forgetstring_encrypt(email=forgetpsw.email.data.lower())
                    this_user.forget = {
                        'string': forgetstring,
                        'time': int(time.time())
                    }
                    this_user.save()
                    mail_send(subject='你好，小熊笔记发来重置密码的密钥串', recipients=[this_user.email], html_body=render_template('mail/user_forgetpassword.html', user={"name": this_user.username, "fstring": forgetstring}))

                    flash(u"已发送密码重置邮件，请前往邮箱查收。邮件一小时内有效")
                    return redirect(url_for('sign_module.forgetpassword_function'))

                else:
                    if now_time - int(this_user.forget['time']) > 3600:
                        # Overtime
                        forgetstring = forget_check.forgetstring_encrypt(email=forgetpsw.email.data.lower())
                        this_user.forget = {
                            'string': forgetstring,
                            'time': int(time.time())
                        }
                        this_user.save()
                        # send mail
                        mail_send(subject='你好，小熊笔记发来重置密码的密钥串', recipients=[this_user.email], html_body=render_template('mail/user_forgetpassword.html', user={"name": this_user.username, "fstring": forgetstring}))

                        flash(u"原密码重置邮件已失效，已重新生成并发送密码重置邮件，请前往邮箱查收")
                        return redirect(url_for('sign_module.forgetpassword_function'))
                    elif (now_time - int(this_user.forget['time']) < 3600) and (now_time - int(this_user.forget['time']) > 60):

                        # send mail
                        this_user.forget['time'] = now_time
                        this_user.save()
                        mail_send(subject='你好，小熊笔记发来重置密码的密钥串', recipients=[this_user.email], html_body=render_template('mail/user_forgetpassword.html', user={"name": this_user.username, "fstring": this_user.forget.string}))

                        flash(u"密码重置邮件已重新发送")
                        return redirect(url_for('sign_module.forgetpassword_function'))
                    elif now_time - int(this_user.forget['time']) < 60:
                        flash(u"密码重置邮件已发送，请勿频繁操作（邮件发送间隔为 1分钟）")
                        return redirect(url_for('sign_module.forgetpassword_function'))

            else:
                flash(u"邮箱尚未注册，或者邮箱异常")
                return redirect(url_for('sign_module.forgetpassword_function'))
        else:
            flash(u"请填写正确的邮箱")
            return redirect(url_for('sign_module.forgetpassword_function'))
    return render_template('users/forgetpassword.html', forgetpsw=forgetpsw)


@sign_module.route('/resetpassword', methods=['GET', 'POST'])
@require_base_domain
@require_not_login
def resetpassword_function():
    forgetstring = request.args.get('forgetstring', '')
    resetform = ResetPswForm(forgetstring=forgetstring)
    reset_check = UserCheck()
    if request.method == 'POST':
        if resetform.validate_on_submit():
            user_count = User.objects(email=resetform.email.data.lower()).count()
            if user_count == 1:
                this_user = User.objects(
                    email=resetform.email.data.lower(),
                    ).first()
                if 'forget' in this_user and this_user.forget['string'] == resetform.forgetstring.data and (int((time.time())) - int(this_user.forget['time']) < 3600):
                    this_user.password = reset_check.password_encrypt(
                        email=resetform.email.data.lower(),
                        password=resetform.password.data)
                    this_user.forget = None
                    this_user.save()
                    flash(u"密码已经修改成功，去登陆吧")
                    return redirect(url_for('sign_module.login_function'))
                else:
                    flash(u"数据匹配失败，请核对你的信息")
                    return redirect(url_for('sign_module.resetpassword_function'))
            else:
                flash(u"邮件验证失败")
                return redirect(url_for('sign_module.resetpassword_function'))
        else:
            flash(u"信息核对失败，密码修改失败，请重新输入")
            return redirect(url_for('sign_module.resetpassword_function'))
    return render_template('users/resetpassword.html', resetform=resetform)


@sign_module.route('/setting/', methods=['GET'])
@require_base_domain
@require_login
def setting_redirect_function():
    return redirect(url_for('sign_module.setting_function', setcate='account'))


@sign_module.route('/setting/<string:setcate>', methods=['GET', 'POST'])
@require_login
def setting_function(setcate):
    def account():
        description_form = SettingAccountForm(descriptions=session['user']['description'])
        if request.method == 'POST':
            if description_form.validate_on_submit():
                this_user = User.objects(email=session['user']['email']).first()
                this_user.description = description_form.descriptions.data
                this_user.save()
                flash(u"个人介绍修改成功。")
                session['user']['description'] = description_form.descriptions.data
                return redirect(url_for('sign_module.setting_function', setcate="account"))
        return render_template('users/setting_account.html', description_form=description_form)

    def password():
        password_form = SettingResetPasswordForm()
        if request.method == 'POST':
            if password_form.validate_on_submit():
                usercheck_d = UserCheck()
                post_password_encrypt = usercheck_d.password_encrypt(
                    email=session['user']['email'],
                    password=password_form.beforepassword.data)
                this_user = User.objects(email=session['user']['email']).first()
                if this_user.password == post_password_encrypt:
                    new_password_encrypt = usercheck_d.password_encrypt(
                        email=session['user']['email'],
                        password=password_form.newpassword.data)
                    this_user.password = new_password_encrypt
                    this_user.save()
                    flash(u"密码修改成功")
                    return redirect(url_for('sign_module.setting_function', setcate="password"))
                else:
                    flash(u"原密码错误，请重试")
                    return redirect(url_for('sign_module.setting_function', setcate="password"))
            else:
                flash(u"数据提交失败，请检查输入内容")
                return redirect(url_for('sign_module.setting_function', setcate="password"))
        return render_template('users/setting_password.html', password_form=password_form)

    def publicsetting():
        CateAddForm = PublicSettingAddCateForm()
        all_cate = NoteCate.objects(belong=User.objects(email=session['user']['email']).first())
        if request.method == 'POST':
            if CateAddForm.validate_on_submit():
                if NoteCate.objects(abbname=CateAddForm.abbname.data).count() == 0 and CateAddForm.abbname.data != '0':
                    NoteCate(
                        name=CateAddForm.name.data,
                        abbname=CateAddForm.abbname.data,
                        belong=User.objects(email=session['user']['email']).first()
                        ).save()
                    flash(u"分类添加成功")
                    return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
                else:
                    flash(u"分类添加失败，分类缩略名已存在，请更换后再重试")
                    return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
            else:
                flash(u"数据添加失败")
                return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
        return render_template('users/setting_publicsetting.html', all_cate=all_cate, CateAddForm=CateAddForm)

    def publicsettingchange():
        change_cate = str(request.args.get('abbname', ''))
        if change_cate == '':
            flash(u"未输入分类缩略名，请正确操作")
            return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
        if not NoteCate.objects(abbname=change_cate, belong=User.objects(email=session['user']['email']).first()).count() == 1:
            flash(u"分类缩略名有误，请正确操作")
            return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))

        this_user_cate = NoteCate.objects(
            abbname=change_cate,
            belong=User.objects(email=session['user']['email']).first()
            ).first()
        CateChangeForm = PublicSettingDeleteCateForm(
            hideabbname=change_cate,
            name=this_user_cate.name,
            abbname=this_user_cate.abbname)
        if request.method == 'POST':
            if CateChangeForm.validate_on_submit():
                if CateChangeForm.hideabbname.data == change_cate:
                    if CateChangeForm.abbname.data == CateChangeForm.hideabbname.data:
                        this_user_cate.name = CateChangeForm.name.data
                        this_user_cate.save()
                        flash(u"分类信息更新成功")
                        return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
                    else:
                        if not NoteCate.objects(abbname=CateChangeForm.abbname.data, belong=User.objects(email=session['user']['email']).first()).count() == 0 and CateChangeForm.abbname.data != '0':
                            flash(u"新的分类缩略名已存在，请使用新的缩略名")
                        else:
                            this_user_cate.name = CateChangeForm.name.data
                            this_user_cate.abbname = CateChangeForm.abbname.data
                            this_user_cate.save()
                            flash(u"分类信息更新成功")
                            return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
                else:
                    flash(u"非法操作。")
                    return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
            else:
                flash(u"数据提交失败，请检查输入")
        return render_template('users/setting_publicsettingchange.html', CateChangeForm=CateChangeForm)

    def publicsettingdelete():
        if request.method == 'GET':
            change_cate = str(request.args.get('abbname', ''))
            if change_cate == '':
                flash(u"未输入分类缩略名，请正确操作")
                return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))

            if not NoteCate.objects(abbname=change_cate, belong=User.objects(email=session['user']['email']).first()).count() == 1:

                flash(u"分类缩略名有误，请正确操作")
                return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))

            this_user_cate = NoteCate.objects(
                abbname=change_cate,
                belong=User.objects(email=session['user']['email']).first()
                ).first()

            other_user_cate = NoteCate.objects(abbname__ne=change_cate, belong=User.objects(email=session['user']['email']).first()).first()
            all_this_cate_note = Note.objects(public_status=NOTECONSTANTS.PUBLIC, public_cate=this_user_cate, belong=User.objects(email=session['user']['email']).first())

            if other_user_cate is None:

                for one_note in all_this_cate_note:
                    one_note.public_status = NOTECONSTANTS.PRIVATE
                    one_note.public_cate = None
                    one_note.save()

                flash(u"分类已删除，因无其他公开分类，该分类下的笔记全部迁移为私有笔记")
            else:

                for one_note in all_this_cate_note:
                    one_note.public_cate = other_user_cate
                    one_note.save()
                flash(u"分类已删除，原分类笔记已迁移至 "+other_user_cate.name)

            NoteCate.delete(this_user_cate)

            return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))
        else:
            flash(u"非法操作。")
            return redirect(url_for('sign_module.setting_function', setcate="publicsetting"))

    def blog():
        blogform = BlogSettingForm()
        if request.method == 'GET':
            this_user_blog = Blog.objects(belong=User.objects(email=session['user']['email']).first()).first()
            if this_user_blog is not None:
                blogform.name.data = this_user_blog.name
                blogform.descriptions.data = this_user_blog.descriptions
                blogform.key.data = this_user_blog.keyword
                blogform.domain.data = ','.join(this_user_blog.domain)
        elif request.method == 'POST':
            if blogform.validate_on_submit():
                all_domain = blogform.domain.data.lower().split(',')
                domain_error_msg = u''
                for one_domain in all_domain:
                    if Blog.objects(domain=one_domain, belong__ne=User.objects(email=session['user']['email']).first()).count() != 0 or one_domain in ['www.bearnote.com', 'bearnote.com']:
                        domain_error_msg = domain_error_msg + str(one_domain) + u"已经存在，请更换; "
                if domain_error_msg == '':
                    print 'success'
                    if Blog.objects(belong=User.objects(email=session['user']['email']).first()).count() == 1:
                        this_user_blog = Blog.objects(belong=User.objects(email=session['user']['email']).first()).first()
                        this_user_blog.name = blogform.name.data
                        this_user_blog.descriptions = blogform.descriptions.data
                        this_user_blog.keyword = blogform.key.data
                        this_user_blog.domain = blogform.domain.data.lower().split(',')
                        this_user_blog.save()
                    else:
                        Blog(name=blogform.name.data, descriptions=blogform.descriptions.data, keyword=blogform.key.data, domain=all_domain, belong=User.objects(email=session['user']['email']).first()).save()

                    # send mail

                    flash(u"博客信息更新成功。")
                    return redirect(url_for('sign_module.setting_function', setcate="blog"))
                else:
                    flash(domain_error_msg)
                    return redirect(url_for('sign_module.setting_function', setcate="blog"))
            else:
                flash(u"信息填写不正确，请检查后重新提交")
                return redirect(url_for('sign_module.setting_function', setcate="blog"))
        return render_template('users/setting_blog.html', blogform=blogform)
        return 'blog'

    SETCATE = {
        'account': account,
        'password': password,
        'publicsetting': publicsetting,
        'publicsettingchange': publicsettingchange,
        'publicsettingdelete': publicsettingdelete,
        'blog': blog
    }

    if setcate in SETCATE:
        return SETCATE.get(setcate)()
    else:
        abort(404)
