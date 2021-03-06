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

    # 分页设置
    PER_PAGE = 10
    HALF_PAGE_DISPLAY = 4  # 当前页码每侧展示的页码个数
    BLOGDOG_THEMES = {
        'Lux': 'Lux',
        'Sketchy': 'Sketchy',
        'Litera': 'Litera',
        'Sandstone': 'Sandstone',  # 褐色颜色很好，部分字体需要调整
        # 'Flatly': 'Flatly',  # 颜色搭配不好

        # 'Minty': 'Minty',   # 太粉嫩
        # 'Journal': 'Journal',  # 颜色不和谐
    }
    BLOGDOG_CODE_STYLE = ['agate', 'dark', 'zenburn']

    # 主题颜色设置

    # 邮件配置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('admin', MAIL_USERNAME)
    BLOGDOG_EMAIL = '2314255424@qq.com'


class DevelopmentConfig(BaseConfig):
    # 本地开发 还是使用 sqlite3 速度快
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(baseDir, 'data-dev.db')
    # 添加七牛云存储
    UEDITOR_QINIU_ACCESS_KEY = "NaTF79Ps5Gx4Ee8LcuhViZHMZQL9ow-tNA-5hwAQ"
    UEDITOR_QINIU_SECRET_KEY = "jjRQRitfFrWoUGfS8rj-sP57mkzhJvshL0rKeMSi"
    UEDITOR_QINIU_BUCKET_NAME = "myfile02-public"
    UEDITOR_QINIU_DOMAIN = "http://cdn.img.pygorun.com/"


class TestingConfig(BaseConfig):
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        SQLALCHEMY_DATABASE_URI = prefix + os.path.join(baseDir, 'data.db')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(baseDir, 'data.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
