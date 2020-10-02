# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1


import os

from flask import Flask
from flask_login import current_user

from blogDog.cli import command, command1, command2, command3
from blogDog.extensions import db, migrate, moment, bootstrap, login_manager, ckeditor, csrf
from blogDog.models import Admin, Post, Category, Comment, Link
from blogDog.settings import config
from blogDog.views import indexView
from blogDog.web.admin import admin_bp
from blogDog.web.auth import auth_bp
from blogDog.web.blog import blog_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 添加一个默认视图； 写项目的时候可以删除
    # with app.app_context():
    #     app.add_url_rule('/', endpoint='index', view_func=indexView)
    register_extensions(app)
    register_commands(app)
    register_blueprint(app)
    register_template_context(app)

    return app


def register_extensions(app):
    # 添加数据库相关扩展
    db.init_app(app)  # 数据库ORM
    migrate.init_app(app, db)  # 数据库版本控制软件
    moment.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)


def register_commands(app):
    """添加终端命令"""
    command(app, db)
    command1(app, db)
    command2(app, db)
    command3(app, db)


def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_shell_context(app):
    """添加flask shell 上下文内容"""

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    """在模板上下文中，添加全局变量"""

    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        subjects = Category.query.filter_by(isSubject=True).all()
        recommends = Post.query.filter_by(isRecommend=True).order_by(Post.timestamp.desc()).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, links=links, recommends=recommends
                    , unread_comments=unread_comments, subjects=subjects)
