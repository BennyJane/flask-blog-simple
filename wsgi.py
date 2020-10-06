# -*- coding: utf-8 -*-
# @Time : 2020/10/6
# @Author : Benny Jane
# @Email : 暂无
# @File : wsgi.py
# @Project : flask-blog-v1

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from blogDog import create_app  # noqa

app = create_app('production')