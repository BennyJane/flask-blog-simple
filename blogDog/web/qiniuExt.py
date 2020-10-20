# -*- coding: utf-8 -*-
# @Time : 2020/10/19
# @Author : Benny Jane
# @Email : 暂无
# @File : qiniuExt.py
# @Project : flask-blog-v1
from io import BytesIO
from urllib import parse

import qiniu
from flask import Blueprint, request, current_app, jsonify

from blogDog import csrf
from blogDog.common.utils import random_filename

qiniu_bp = Blueprint('qiniu', __name__)


@csrf.exempt
@qiniu_bp.route('/image', methods=['GET', 'POST'])
def upload():
    UEDITOR_QINIU_ACCESS_KEY = current_app.config["UEDITOR_QINIU_ACCESS_KEY"]
    UEDITOR_QINIU_SECRET_KEY = current_app.config["UEDITOR_QINIU_SECRET_KEY"]
    UEDITOR_QINIU_BUCKET_NAME = current_app.config["UEDITOR_QINIU_BUCKET_NAME"]
    UEDITOR_QINIU_DOMAIN = current_app.config["UEDITOR_QINIU_DOMAIN"]

    img = request.files.get('editormd-image-file')
    filename = img.filename
    save_filename = random_filename(filename)
    result = {
        'success': 0,
        'message': '',
        'url': ''
    }
    q = qiniu.Auth(UEDITOR_QINIU_ACCESS_KEY, UEDITOR_QINIU_SECRET_KEY)
    token = q.upload_token(UEDITOR_QINIU_BUCKET_NAME)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    ret, info = qiniu.put_data(token, save_filename, buffer.read())
    if info.ok:
        result['url'] = parse.urljoin(UEDITOR_QINIU_DOMAIN, ret['key'])
    else:
        result['success'] = 1
        result['message'] = ''
    print(result)
    return jsonify(result)
