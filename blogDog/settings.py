# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : settings.py
# @Project : flask-blog-v1
import os
import sys

# 考虑直接使用app的root_path 路径
baseDir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig(object):
    PROJECT_NAME = 'blogDog'

    SECRET_KEY = os.getenv("SECRET_KEY", 'dey key')
    IS_DEBUG = True

    SQLALCHEMY_DATABASE_URI = prefix + ":memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True




class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(baseDir, 'data-dev.db')




class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(baseDir, 'data-test.db')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(baseDir, 'data.db')



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
