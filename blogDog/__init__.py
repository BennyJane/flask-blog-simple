# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1


import os

from flask import Flask
from blogDog.settings import config
from blogDog.views import indexView

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    with app.app_context():
        app.add_url_rule('/', endpoint='/', view_func=indexView)
    return app


# 必须将试图函数全部引入到__init__文件内 ==》 将视图函数引入到app实例化的文件内
import blogDog.views

if __name__ == '__main__':
    app.run()
