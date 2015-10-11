# -*- coding: utf-8 -*-
from flask import Blueprint, request, session, redirect, \
    flash, url_for, render_template
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

note_module = Blueprint('note_module', __name__)


# 新建笔记函数
@note_module.route('/new', methods=['GET', 'POST'])
@require_base_domain
@require_login
def note_new_function():

    # 初始化 笔记表单的公开分类
    note_new_form = NoteForm()
    note_new_form.public.choices = [('0', u"私有笔记,不公开")]
    for c in NoteCate.objects(belong=User.objects(
            email=session['user']['email']).first()):

        note_new_form.public.choices.append((c.abbname, c.name))

    # 数据提交处理
    if request.method == 'POST':
        if note_new_form.validate_on_submit():
            # 公开分类处理
            if note_new_form.public.data != '0':
                public_status = '1'
                public_cate = NoteCate.objects(
                    abbname=note_new_form.public.data,
                    belong=User.objects(email=session['user']['email']).first()
                ).first()
            else:
                public_status = '0'
                public_cate = None

            # 保存笔记
            Note(
                noteid=getnextseq(),
                title=note_new_form.title.data,
                subtitle=note_new_form.subtitle.data,
                content=note_new_form.content.data,
                public_status=public_status,
                public_cate=public_cate,
                tag=note_new_form.tag.data.split(","),
                belong=(User.objects(email=session['user']['email']).first())
            ).save()

            return redirect(url_for('note_module.note_new_function'))

        # 数据填写不完整
        else:
            flash(u"内容填写不完整")
            return redirect(url_for('note_module.note_new_function'))
        return render_template('note/note_new.html',
                               note_new_form=note_new_form)


# 我的笔记 页面函数
@note_module.route('/mynote', methods=['GET'])
@require_base_domain
@require_login
def mynote_function():

    # 分页设置
    note_count = Note.objects(belong=User.objects(
        email=session['user']['email']).first()).count()

    if note_count % NOTECONSTANTS.PER_PAGE_COUNT:
        page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1
    else:
        page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT

    if note_count == 0:
        page_count += 1

    # 读取分页
    now_page = request.args.get('page', 1)
    try:
        now_page = int(now_page)
    except:
        return redirect(url_for('note_module.mynote_function'))

    if now_page >= 1 and now_page <= page_count:
        now_page = now_page
    else:
        return redirect(url_for('note_module.mynote_function',
                                page=page_count))

    # 读取该页笔记
    now_page_note = Note.objects(
        belong=User.objects(email=session['user']['email']).first()
    ).skip(NOTECONSTANTS.PER_PAGE_COUNT * (now_page - 1)
           ).limit(NOTECONSTANTS.PER_PAGE_COUNT)

    return render_template('note/my-note.html',
                           notes=now_page_note,
                           page_info={'page_count': page_count,
                                      'now_page': now_page}
                           )

# 笔记墙 页面函数


@note_module.route('/note/', methods=['GET'])
@require_base_domain
def note_wall_function():

    # 分页设置
    note_count = Note.objects(belong=User.objects(
        email=session['user']['email']).first()).count()

    if note_count % NOTECONSTANTS.PER_PAGE_COUNT:
        page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1
    else:
        page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT

    if note_count == 0:
        page_count += 1

    # 读取当前分页
    now_page = request.args.get('page', 1)
    try:
        now_page = int(now_page)
    except:
        return redirect(url_for('note_module.note_wall_function'))
    if now_page >= 1 and now_page <= page_count:
        now_page = now_page
    else:
        return redirect(url_for('note_module.note_wall_function',
                                page=page_count))

    now_page_note = Note.objects(
        public_status=NOTECONSTANTS.PUBLIC
    ).skip(NOTECONSTANTS.PER_PAGE_COUNT * (now_page - 1)
           ).limit(NOTECONSTANTS.PER_PAGE_COUNT)

    # 读取当前分页笔记的评论
    for one_note in now_page_note:
        one_note.comment_num = Comment.objects(noteid=one_note.noteid).count()

    return render_template('note/note_wall.html',
                           notes=now_page_note,
                           page_info={
                               'page_count': page_count,
                               'now_page': now_page}
                           )


# 单一笔记 页面函数
@note_module.route("/note/<int:noteid>", methods=['GET', 'POST'])
def one_note_function(noteid):

    # 笔记存在性判断
    if Note.objects(noteid=noteid).count() == 0:
        flash(u"找不到这篇文章，不要乱来了。")
        return redirect(url_for('note_module.note_wall_function'))

    # 读取该笔记
    this_note = Note.objects(noteid=noteid).first()

    # MarkDown 渲染笔记正文
    renderer = mistune.Renderer(escape=True, hard_wrap=True)
    markdown = mistune.Markdown(renderer=renderer)
    this_note.content = markdown(this_note.content)

    # 笔记作者邮件MD5 用于显示头像
    this_note.belong.email_md5 = common.md5_encrypt(this_note.belong.email)

    # 笔记权限判断
    if this_note.public_status == NOTECONSTANTS.PRIVATE and \
            session['user']['role'] == USERCONSTANTS.USER:

        # 登陆 与 非登陆 跳转页面不同
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

        # 提交评论
        if comment.validate_on_submit():
            Comment(name=comment.name.data,
                    email=comment.email.data.lower(),
                    domain=comment.domain.data,
                    content=comment.content.data,
                    noteid=noteid,).save()

            return redirect(url_for('note_module.one_note_function',
                                    noteid=noteid))
        else:
            flash(u"内容填写不完整")
            return redirect(url_for('note_module.one_note_function',
                                    noteid=noteid))

    # 读取当前笔记的所有评论
    all_comment = Comment.objects(noteid=noteid)

    # 评论Email添加MD5 用于头像显示
    for one_comment in all_comment:
        one_comment.email_md5 = common.md5_encrypt(one_comment.email)

    return render_template('/note/one_note.html',
                           this_note=this_note,
                           comment=comment,
                           all_comment=all_comment
                           )

# 笔记编辑


@note_module.route("/note/edit/<int:noteid>", methods=['GET', 'POST'])
@require_base_domain
@require_login
def note_edit_function(noteid):

    # 笔记存在性判断
    if Note.objects(noteid=noteid,
                    belong=User.objects(email=session['user']['email']).first()
                    ).count() == 0:

        flash(u"找不到这篇文章，不要乱来了。")
        return redirect(url_for('note_module.mynote_function'))

    # 读取该笔记
    this_note = Note.objects(noteid=noteid).first()

    # 编辑表单 设置
    note_edit_form = NoteForm(
        title=this_note.title,
        subtitle=this_note.subtitle,
        content=this_note.content,
        tag=",".join(this_note.tag)
    )
    # 加载笔记公开分类
    note_edit_form.public.choices = [('0', u"私有笔记,不公开")]
    for c in NoteCate.objects(belong=User.objects(
        email=session['user']['email']
    ).first()):
        note_edit_form.public.choices.append((c.abbname, c.name))

    # 当GET页面时 显示默认的笔记分类
    if request.method == 'GET' and \
            this_note.public_status == NOTECONSTANTS.PUBLIC:

        note_edit_form.public.data = this_note.public_cate.abbname

    # 数据提交检验
    if request.method == 'POST':

        if note_edit_form.validate_on_submit():

            # 数据提交
            this_note.title = note_edit_form.title.data
            this_note.subtitle = note_edit_form.subtitle.data
            this_note.subtitle = note_edit_form.subtitle.data
            this_note.content = note_edit_form.content.data
            this_note.tag = note_edit_form.tag.data.split(',')
            if note_edit_form.public.data != '0':
                this_note.public_status = '1'
                this_note.public_cate = NoteCate.objects(
                    abbname=note_edit_form.public.data,
                    belong=User.objects(email=session['user']['email']).first()
                ).first()
            else:
                this_note.public_status = '0'
                this_note.public_cate = None
            this_note.save()
            flash(u"笔记修改成功")
            return redirect(url_for('note_module.one_note_function',
                                    noteid=this_note.noteid))

        else:
            flash(u"笔记内容不完整")

    return render_template('/note/note_edit.html',
                           note_edit_form=note_edit_form,
                           this_note=this_note)

# 笔记删除


@note_module.route('/note/delete/<int:noteid>', methods=['GET'])
@require_base_domain
@require_login
def note_delete_function(noteid):

    # 笔记存在性判断
    if Note.objects(noteid=noteid,
                    belong=User.objects(email=session['user']['email']).first()
                    ).count() == 0:
        flash(u"找不到这篇文章，不要乱来了。")
    return redirect(url_for('note_module.mynote_function'))

    # 删除笔记
    this_note = Note.objects(noteid=noteid, belong=User.objects(
        email=session['user']['email']).first()).first()
    Note.delete(this_note)

    # 删除笔记下的评论
    for one_comment in Comment.objects(noteid=noteid):
        Comment.delete(one_comment)

    flash(u"笔记删除成功")
    return redirect(url_for('note_module.mynote_function'))
