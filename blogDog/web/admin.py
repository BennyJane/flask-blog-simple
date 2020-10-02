# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : blog.py
# @Project : flask-blog-v1

from flask import request, current_app, Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required

from blogDog import Post, Category, db, Link
from blogDog.common.Helper import iPagination
from blogDog.common.utils import redirect_back
from blogDog.forms import PostForm, CategoryForm, LinkForm

admin_bp = Blueprint('admin', __name__)

'''
==================================================================== manage 
'''


@admin_bp.route('/post/manager')
@login_required
def manager_post():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PER_PAGE']  # 考虑字符串问题
    half_page_display = int(current_app.config["HALF_PAGE_DISPLAY"])

    query = Post.query.order_by(Post.timestamp.desc())

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
    return render_template('admin/manage_post.html', page=page, page_params=page_params, posts=posts)


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    # 变量已经被加载到 模板中了
    return render_template('admin/manage_category.html')


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')


# todo 简化代码
'''
==================================================================== new 
# todo 考虑合并这三个函数的前端页面 与 后端功能 
'''


@admin_bp.route('/post/new', methods=['GET', "POST"])
@login_required
def new_post():
    form = PostForm()
    print(form.category.choices)
    if form.validate_on_submit():
        title = form.title.data
        sub_title = form.sub_title.data
        # 前端传入的是 分类的id
        category = Category.query.get(form.category.data)
        can_comment = form.can_comment.data
        isRecommend = form.isRecommend.data
        body = form.body.data
        post = Post(title=title, body=body, category=category,
                    sub_title=sub_title, can_comment=can_comment, isRecommend=isRecommend)
        db.session.add(post)
        db.session.commit()
        flash("添加新文章", "success")
        return redirect(url_for("blog.show_post", post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/category/new', methods=['GET', "POST"])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        isSubject = form.isSubject.data
        subject_info = form.subject_info.data

        is_exist = Category.query.filter_by(name=name).first()
        if is_exist:
            flash("该分类已经存在", "waring")
            return redirect(url_for("admin.new_category"))
        category = Category(name=name, isSubject=isSubject, subject_info=subject_info)
        db.session.add(category)
        db.session.commit()
        flash("添加成功", "success")
        return redirect(url_for("admin.manage_category"))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/link/new', methods=['GET', "POST"])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        message = form.message.data

        link = Link(name=name, url=url, message=message)
        db.session.add(link)
        db.session.commit()
        flash("添加成功", "success")
        return redirect(url_for("admin.manage_link"))
    return render_template('admin/new_link.html', form=form)


'''
==================================================================== edit
'''


# todo 可以将其与 新增接口合并
@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        # 更新内容
        post.title = form.title.data
        post.sub_title = form.sub_title.data
        # 前端传入的是 分类的id
        post.category = Category.query.get(form.category.data)
        post.can_comment = form.can_comment.data
        post.isRecommend = form.isRecommend.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash("修改成功", "success")
        return redirect(url_for("blog.show_post", post_id=post.id))
    form.title.data = post.title
    form.sub_title.data = post.sub_title
    # 传入的是 分类的id
    form.category.data = post.category.id
    form.can_comment.data = post.can_comment
    form.isRecommend.data = post.isRecommend
    form.body.data = post.body
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("删除成功", "success")
    return redirect_back()


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        category.isSubject = form.isSubject.data
        category.subject_info = form.subject_info.data
        db.session.add(category)
        db.session.commit()
        flash("修改成功", "success")
        return redirect(url_for("admin.manage_category"))
    form.name.data = category.name
    form.isSubject.data = category.isSubject
    form.subject_info.data = category.subject_info
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("删除成功", "success")
    return redirect(url_for("admin.manage_category"))


@admin_bp.route('/link/<link_id>/edit', methods=['GET', "POST"])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        link.message = form.message.data

        db.session.add(link)
        db.session.commit()
        flash("更新成功", "success")
        return redirect(url_for("admin.manage_link"))
    form.name.data = link.name
    form.url.data = link.url
    form.message.data = link.message
    return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Category.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash("删除成功", "success")
    return redirect(url_for("admin.manage_link"))
