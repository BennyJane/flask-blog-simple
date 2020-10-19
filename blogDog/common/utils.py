# -*- coding: utf-8 -*-
# @Time : 2020/10/2
# @Author : Benny Jane
# @Email : 暂无
# @File : utils.py
# @Project : flask-blog-v1
import hashlib
import os
import random
import string
import time

from flask import request, redirect, url_for

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    # netloc 服务器位置
    # scheme 获取网络协议
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def register_app_filter(app):
    @app.template_filter()
    def randomLink(links):
        link = random.choice(links)
        res = {
            'title': link.title,
            'body': link.body,
            'id': link.id,
        }
        # print(res)
        return res


def random_filename(rawFileName):
    letters = string.ascii_letters
    salt_string = str(time.time()) + ''.join(random.sample(letters, 5))
    new_filename = hashlib.md5(salt_string.encode('utf-8')).hexdigest()
    ext = os.path.splitext(rawFileName)[-1]
    return new_filename + ext
