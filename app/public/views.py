# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,flash,url_for,session
from app.users.models import *
from app.note.models import *
from app.note import constants as NOTECONSTANTS

from app.public import lib as PublicLib

public_module = Blueprint('public_module',__name__)


@public_module.route('/member/<string:username>',methods=['GET'])

def member_page_function(username = "admin"):

    this_user = PublicLib.get_user(username)
    if this_user == 0:return render_template('404.html'),404


    if Blog.objects(belong=this_user).count() == 1:
    	this_blog = Blog.objects(belong=this_user).first()
    else:
    	this_blog = Blog()
    	this_blog.name = this_user.username
    	this_blog.descriptions = this_user.description
    # 笔记分页
    note_count = Note.objects(public_status=NOTECONSTANTS.PUBLIC,belong=this_user).count()
    page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1 if note_count % NOTECONSTANTS.PER_PAGE_COUNT else note_count / NOTECONSTANTS.PER_PAGE_COUNT
    if note_count == 0:
        page_count += 1
    now_page = request.args.get('page',1)
    try:
        now_page = int(now_page)
    except:
        return redirect(url_for('public_module.member_page_function',username=username))
   
    if now_page >=1 and now_page <= page_count:
        now_page = now_page
    else:
        return redirect(url_for('public_module.member_page_function',username=username,page=page_count))
    now_page_note = Note.objects(public_status=NOTECONSTANTS.PUBLIC,belong=this_user).skip(NOTECONSTANTS.PER_PAGE_COUNT*(now_page-1)).limit(NOTECONSTANTS.PER_PAGE_COUNT)
    # 用户笔记公开分类
    all_cate = NoteCate.objects(belong=this_user)
        
    return render_template('public/index.html',this_user=this_user, this_blog=this_blog, all_cate=all_cate,note=now_page_note,page_info = {'page_count':page_count,'now_page':now_page})


@public_module.route('/member/<string:username>/cate/<string:cate>',methods=['GET'])

def member_cate_function(username,cate):
    # 用户存在性判断
    this_user = PublicLib.get_user(username)
    if this_user == 0: return render_template('404.html'),404

    if Blog.objects(belong=this_user).count() == 1:
        this_blog = Blog.objects(belong=this_user).first()
    else:
        this_blog = Blog()
        this_blog.name = this_user.username
        this_blog.descriptions = this_user.description

    # 用户分类存在性判断
    this_cate = PublicLib.get_cate(this_user,cate)
    if this_cate == 0: return render_template('404.html'),404

    # 用户笔记公开分类
    all_cate = NoteCate.objects(belong=this_user)

    # 笔记分页
    note_count = Note.objects(public_status=NOTECONSTANTS.PUBLIC,belong=this_user,public_cate=this_cate).count()
    page_count = note_count / NOTECONSTANTS.PER_PAGE_COUNT + 1 if note_count % NOTECONSTANTS.PER_PAGE_COUNT else note_count / NOTECONSTANTS.PER_PAGE_COUNT
    if note_count == 0:
        page_count += 1
    now_page = request.args.get('page',1)
    try:
        now_page = int(now_page)
    except:
        return redirect(url_for('public_module.member_page_function',username=username))
   
    if now_page >=1 and now_page <= page_count:
        now_page = now_page
    else:
        return redirect(url_for('public_module.member_page_function',username=username,page=page_count))
    
    # 当页笔记
    now_page_note = Note.objects(public_status=NOTECONSTANTS.PUBLIC,belong=this_user,public_cate=this_cate).skip(NOTECONSTANTS.PER_PAGE_COUNT*(now_page-1)).limit(NOTECONSTANTS.PER_PAGE_COUNT)


    return render_template('public/cate.html',this_user=this_user,this_blog=this_blog,this_cate=this_cate, all_cate=all_cate, note=now_page_note,page_info = {'page_count':page_count,'now_page':now_page})