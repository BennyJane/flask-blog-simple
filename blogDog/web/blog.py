# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : blog.py
# @Project : flask-blog-v1

from flask import Blueprint, request, render_template, current_app

from blogDog import Post, Category, Comment
from blogDog.common.Helper import iPagination

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

    return render_template('blog/post.html', page_params=page_params, comments=comments, post=post)
