# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1


import os

from flask import Flask

from blogDog.cli import command, command1, command2, command3
from blogDog.extensions import db, migrate
from blogDog.settings import config
from blogDog.views import indexView


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 添加一个默认视图； 写项目的时候可以删除
    with app.app_context():
        app.add_url_rule('/', endpoint='index', view_func=indexView)
    register_extensions(app)
    register_commands(app)

    return app


def register_extensions(app):
    # 添加数据库相关扩展
    db.init_app(app)  # 数据库ORM
    migrate.init_app(app, db)  # 数据库版本控制软件


def register_commands(app):
    command(app)
    command1(app)
    command2(app)
    command3(app)

