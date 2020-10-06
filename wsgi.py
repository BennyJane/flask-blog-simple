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

# 这种写法会导致本地生成 produce 的文件
# app = create_app('production')
app = create_app()


#SECRET_KEY=DJFWLSFJDLSADFDK134545615466
#FLASK_ENV=production
#MAIL_SERVER=smtp.qq.com
#MAIL_USERNAME=2314255424@qq.com
#MAIL_PASSWORD=phoeeizhwkhqebbj
