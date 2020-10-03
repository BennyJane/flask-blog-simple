# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
# 需要添加，才能在前端页面使用
ckeditor = CKEditor()
csrf = CSRFProtect()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    # todo 这个文件引入必须放在这里， 不能放到全局
    from blogDog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# 是视图函数内定义，就不需要再在这里写了
# login_manager.login_message = 'A Dog，欢迎回来！'
login_manager.login_message_category = 'warning'
