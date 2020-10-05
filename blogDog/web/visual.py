# -*- coding: utf-8 -*-
# @Time : 2020/10/4
# @Author : Benny Jane
# @Email : 暂无
# @File : taskAndlinks.py
# @Project : flask-blog-v1
from flask import Blueprint, render_template

visual_bp = Blueprint('visual', __name__)


@visual_bp.route('/list', methods=['GET', 'POST'])
def index():
    return render_template('visual/index.html')
