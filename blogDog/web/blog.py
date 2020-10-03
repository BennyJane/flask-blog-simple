# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : blog.py
# @Project : flask-blog-v1
from flask import Blueprint, request, render_template, current_app, flash, redirect, url_for
from flask_login import current_user

from blogDog.common.Helper import iPagination
from blogDog.email import send_new_comment_email, send_new_reply_email
from blogDog.extensions import db, csrf
from blogDog.forms import CommentForm, AdminCommentForm
from blogDog.models import Post, Category, Comment

blog_bp = Blueprint('blog', __name__)
'''
 不能放在全局内， 因为此时 current_app 没有指向性 ==》 上下文的问题
per_page = current_app.config['PER_PAGE']  # 考虑字符串问题
half_page_display = int(current_app.config["HALF_PAGE_DISPLAY"])
'''


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.timestamp.desc())
    per_page = current_app.config['PER_PAGE']  # 考虑字符串问题
    half_page_display = int(current_app.config["HALF_PAGE_DISPLAY"])

    page_params = {
        'total': query.count(),
        'page_size': per_page,
        'half_page_display': half_page_display,
        'page': page,
        'url': request.full_path.replace('&page={}'.format(page), "")  # 清空页码
    }
    page_params = iPagination(page_params)
    # 筛选当前页面的数据
    offset = (page - 1) * per_page
    posts = query.offset(offset).limit(per_page).all()

    return render_template('blog/index.html', page_params=page_params, posts=posts)


@blog_bp.route('/subject')
def subject():
    return '未实现'


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']  # 考虑字符串问题
    half_page_display = int(current_app.config["HALF_PAGE_DISPLAY"])
    if category.isSubject:
        # 专题文航按照名称排序，方便文章序列的良好化
        query = Post.query.with_parent(category).order_by(Post.title.asc())
    else:
        query = Post.query.with_parent(category).order_by(Post.timestamp.desc())
    # 源码中提供的方法
    page_params = {
        'total': query.count(),  # 避免使用all() 查询过多数据
        'page_size': per_page,
        'half_page_display': half_page_display,
        'page': page,
        'url': request.full_path.replace('&page={}'.format(page), "")  # 清空页码
    }
    page_params = iPagination(page_params)
    # 筛选当前页面的数据
    offset = (page - 1) * per_page
    posts = query.offset(offset).limit(per_page).all()

    return render_template('blog/category.html', category=category, page_params=page_params, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']  # 考虑字符串问题
    half_page_display = int(current_app.config["HALF_PAGE_DISPLAY"])

    query = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc())

    page_params = {
        'total': query.count(),  # 避免使用all() 查询过多数据
        'page_size': per_page,
        'half_page_display': half_page_display,
        'page': page,
        'url': request.full_path.replace('&page={}'.format(page), "")  # 清空页码
    }
    page_params = iPagination(page_params)
    # 筛选当前页面的数据
    offset = (page - 1) * per_page
    comments = query.offset(offset).limit(per_page).all()

    # FIXME 处理用户评论的操作
    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLOGDOG_EMAIL']
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        body = form.body.data
        comment = Comment(author=author, email=email, body=body, post=post,
                          from_admin=from_admin, reviewed=reviewed)
        # FIXME 注意被回复对象的ID是如何获取的
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            #  TODO 发送邮件
            send_new_reply_email(replied_comment)

        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash("评论完成", "success")
        else:
            flash("评论已完成，等待审核中，感谢你的参与。", "info")
            # todo 发送邮件
            send_new_comment_email(post)
        return redirect(url_for(".show_post", post_id=post_id))

    return render_template('blog/post.html', page_params=page_params, comments=comments, post=post, form=form)


@blog_bp.route('/reply/comment/<int:comment_id>', methods=['GET', 'POST'])
def reply_comment(comment_id):
    """该函数用来判断文章是否可以评论； 当可以评论的时候，页面滚动到评论表单处"""
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash("文章关闭评论功能", 'warning')
        return redirect(url_for(".show_post", post_id=comment.post_id))
    # fixme author 该参数没有被后端处理，直接在模板中，通过 request.args.get() 获取
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


'''
==================================================================== search
1. 标题内容
'''


# 没有使用 Flask-Forms； 所以需要关闭 csrf的保护
@blog_bp.route('/search/post', methods=['GET', 'POST'])
@csrf.exempt
def search_post():
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        targetText = request.form.get('search')
    else:
        targetText = request.args.get('search')
    query = Post.query.filter(Post.title.like(f'%{targetText}%')).order_by(Post.timestamp.desc())
    per_page = current_app.config['PER_PAGE']  # 考虑字符串问题
    half_page_display = int(current_app.config["HALF_PAGE_DISPLAY"])

    # FIXME 页面跳转链接设置
    page_url = request.full_path.replace('&page={}'.format(page), "").replace('&search={}'.format(targetText), "")

    page_params = {
        'total': query.count(),
        'page_size': per_page,
        'half_page_display': half_page_display,
        'page': page,
        'url': page_url + f'&search={targetText}'  # 清空页码
    }
    page_params = iPagination(page_params)
    # 筛选当前页面的数据
    offset = (page - 1) * per_page
    posts = query.offset(offset).limit(per_page).all()

    return render_template('blog/index.html', page_params=page_params, posts=posts)
