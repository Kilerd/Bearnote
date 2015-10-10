# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,flash,url_for,session
from app.note.models import *
from app.users.decorators import require_login
from app.users.models import User
from app.note.forms import NoteForm, CommentForm
from app.note import constants as NOTECONSTANTS
from app.users import constants as USERCONSTANTS
from app.note.lib import getnextseq
from app.lib import common
from app.common.decorators import require_base_domain

import mistune

note_module = Blueprint('note_module',__name__)


@note_module.route('/new',methods=['GET','POST'])
@require_base_domain
@require_login
def note_new_function():
    note_new_form = NoteForm()
    note_new_form.public.choices = [('0',u"私有笔记,不公开")]
    for c in NoteCate.objects(belong = User.objects(email = session['user']['email']).first()):
        note_new_form.public.choices.append((c.abbname,c.name))
    if note_new_form.validate_on_submit():
        if note_new_form.public.data != '0':
            public_status = '1'
            public_cate = NoteCate.objects(abbname = note_new_form.public.data,belong = User.objects(email = session['user']['email']).first()).first()
        else:
            public_status = '0'
            public_cate = None

        Note(
            noteid=getnextseq(),
            title=note_new_form.title.data,
            subtitle=note_new_form.subtitle.data,
            content = note_new_form.content.data,
            public_status = public_status,
            public_cate = public_cate,
            tag = note_new_form.tag.data.split(","),
            belong = (User.objects(email=session['user']['email']).first())
            ).save()

        return redirect(url_for('note_module.note_new_function'))
    return render_template('note/note_new.html',note_new_form = note_new_form)


@note_module.route('/mynote',methods=['GET'])
@require_base_domain
@require_login
def mynote_function():
    # Page Control
    note_count = Note.objects(belong=User.objects(email=session['user']['email']).first()).count()
    page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1 if note_count % NOTECONSTANTS.PER_PAGE_COUNT else note_count / NOTECONSTANTS.PER_PAGE_COUNT
    if note_count == 0:
        page_count += 1
    now_page = request.args.get('page',1)
    try:
        now_page = int(now_page)
    except:
        return redirect(url_for('note_module.mynote_function'))
    if now_page >=1 and now_page <= page_count:
        now_page = now_page
    else:
        return redirect(url_for('note_module.mynote_function',page=page_count))
    now_page_note = Note.objects(belong=User.objects(email=session['user']['email']).first()).skip(NOTECONSTANTS.PER_PAGE_COUNT*(now_page-1)).limit(NOTECONSTANTS.PER_PAGE_COUNT)
    return render_template('note/my-note.html',notes = now_page_note,page_info = {'page_count':page_count,'now_page':now_page})


@note_module.route('/note/',methods=['GET'])
@require_base_domain
def note_wall_function():
    note_count = Note.objects(public_status=NOTECONSTANTS.PUBLIC).count()
    page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1 if note_count % NOTECONSTANTS.PER_PAGE_COUNT else note_count / NOTECONSTANTS.PER_PAGE_COUNT
    if note_count == 0:
        page_count += 1
    now_page = request.args.get('page',1)
    try:
        now_page = int(now_page)
    except:
        return redirect(url_for('note_module.note_wall_function'))
    if now_page >=1 and now_page <= page_count:
        now_page = now_page
    else:
        return redirect(url_for('note_module.note_wall_function',page=page_count))
    now_page_note = Note.objects(public_status=NOTECONSTANTS.PUBLIC).skip(NOTECONSTANTS.PER_PAGE_COUNT*(now_page-1)).limit(NOTECONSTANTS.PER_PAGE_COUNT)
    return render_template('note/note_wall.html',notes = now_page_note,page_info = {'page_count':page_count,'now_page':now_page})





@note_module.route("/note/<int:noteid>",methods=['GET','POST'])
def one_note_function(noteid):

    if Note.objects(noteid=noteid).count() == 0:
        flash(u"找不到这篇文章，不要乱来了。")
        return redirect(url_for('note_module.note_wall_function'))
    else:
        this_note = Note.objects(noteid=noteid).first()
        renderer = mistune.Renderer(escape=True, hard_wrap=True)
        # use this renderer instance
        markdown = mistune.Markdown(renderer=renderer)

        this_note.content = markdown(this_note.content)
        this_note.belong.email_md5 = common.md5_encrypt(this_note.belong.email)
        
        # 笔记权限判断
        if this_note.public_status == NOTECONSTANTS.PRIVATE and session['user']['role'] == USERCONSTANTS.USER:
            
            if 'user' in session:
                if this_note.belong.email != session['user']['email']:
                    flash(u"无权限查看他人的私有笔记。")
                    return redirect(url_for('note_module.mynote_function'))
            else:
                flash(u"你想查看的笔记为私有笔记，无权限查看。")
                return redirect(url_for('note_module.note_wall_function'))


        # 评论功能
        # 需要添加进session 保存最后一次评论的个人信息
        comment = CommentForm()

        # POST 页面
        if request.method == 'POST':

            # 私有笔记 权限判断
            if this_note.public_status == NOTECONSTANTS.PRIVATE:
                flash(u"该笔记为私有笔记，无法评论。")
                return redirect(url_for('note_module.note_wall_function'))
            

            if comment.validate_on_submit():
                Comment(name = comment.name.data,
                    email = comment.email.data.lower(),
                    domain = comment.domain.data,
                    content = comment.content.data,
                    noteid = noteid,).save()

                return redirect(url_for('note_module.one_note_function',noteid=noteid))
            else:
                flash(u"内容填写不完整")
                return redirect(url_for('note_module.one_note_function',noteid=noteid))
        

        # 读取当前笔记的所有评论
        all_comment = Comment.objects(noteid = noteid)
        
        # 评论Email添加MD5 用于头像显示
        all_comment_ = []
        for one_comment in all_comment:
            one_comment.email_md5 = common.md5_encrypt(one_comment.email)
            all_comment_.append(one_comment)


        return render_template('/note/one_note.html',this_note=this_note, comment=comment, all_comment=all_comment_)


@note_module.route("/note/edit/<int:noteid>",methods=['GET','POST'])
@require_base_domain
@require_login
def note_edit_function(noteid):
    if Note.objects(noteid=noteid,belong=User.objects(email=session['user']['email']).first()).count() == 0:
        flash(u"找不到这篇文章，不要乱来了。")
        return redirect(url_for('note_module.mynote_function'))
    else:
        this_note = Note.objects(noteid=noteid).first()
        note_edit_form = NoteForm(
            title = this_note.title,
            subtitle = this_note.subtitle,
            content = this_note.content,
            tag = ",".join(this_note.tag)
            )
        note_edit_form.public.choices = [('0',u"私有笔记,不公开")]
        for c in NoteCate.objects(belong = User.objects(email = session['user']['email']).first()):
            note_edit_form.public.choices.append((c.abbname,c.name))

        if request.method == 'GET' and this_note.public_status == NOTECONSTANTS.PUBLIC:
            note_edit_form.public.data = this_note.public_cate.abbname

        if request.method == 'POST':
            if note_edit_form.validate_on_submit():
                this_note.title = note_edit_form.title.data
                this_note.subtitle = note_edit_form.subtitle.data
                this_note.subtitle = note_edit_form.subtitle.data
                this_note.content = note_edit_form.content.data
                this_note.tag = note_edit_form.tag.data.split(',')
                print note_edit_form.public.data
                if note_edit_form.public.data != '0':
                    print 'this for public'
                    public_status = '1'
                    public_cate = NoteCate.objects(abbname = note_edit_form.public.data,belong = User.objects(email = session['user']['email']).first()).first()
                else:
                    print 'this for private'
                    public_status = '0'
                    public_cate = None

                print public_status
                this_note.public_status = public_status
                this_note.public_cate = public_cate
                this_note.save()
                flash(u"笔记修改成功")
                return redirect(url_for('note_module.one_note_function',noteid=this_note.noteid))
            else:
                flash(u"笔记内容不完整")

        return render_template('/note/note_edit.html',note_edit_form=note_edit_form,this_note=this_note)

@note_module.route('/note/delete/<int:noteid>',methods=['GET'])
@require_base_domain
@require_login
def note_delete_function(noteid):
    if Note.objects(noteid=noteid,belong=User.objects(email=session['user']['email']).first()).count() == 0:
        flash(u"找不到这篇文章，不要乱来了。")
        return redirect(url_for('note_module.mynote_function'))
    this_note = Note.objects(noteid=noteid,belong=User.objects(email=session['user']['email']).first()).first()
    Note.delete(this_note)
    #Delete Commit
    flash(u"笔记删除成功")
    return redirect(url_for('note_module.mynote_function'))