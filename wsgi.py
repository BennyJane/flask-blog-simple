# -*- coding: utf-8 -*-
# @Time : 2020/10/6
# @Author : Benny Jane
# @Email : 暂无
# @File : wsgi.py
# @Project : flask-blog-v1

import os
from dotenv import load_dotenv

# TODO 是否有必要写个加载方法 ==》 flask 自己会去搜索 .env  .flaskenv 文件
# __file__ 获取当前文件名称 wsgi.py
#  os.path.dirname()   文件目录名 ， 空
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')   # 结果 .env ; 加载当前目录中的.env 文件
# print(dotenv_path)
# print(__file__)
# print(os.path.dirname(__file__))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from blogDog import create_app  # noqa

# 这种写法会导致本地生成 produce 的文件
# app = create_app('production')
# app = create_app()



