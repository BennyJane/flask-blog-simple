# -*- coding: utf-8 -*-
# @Time : 2020/10/4
# @Author : Benny Jane
# @Email : 暂无
# @File : taskAndlinks.py
# @Project : flask-blog-v1
from flask import Blueprint, render_template

task_bp = Blueprint('task', __name__)


@task_bp.route('/list', methods=['GET', 'POST'])
def index():
    # render_template() 文件路径开头可以没有斜杠
    return render_template('task/index.html')