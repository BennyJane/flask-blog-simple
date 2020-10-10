# -*- coding: utf-8 -*-
# @Time : 2020/10/4
# @Author : Benny Jane
# @Email : 暂无
# @File : taskAndlinks.py
# @Project : flask-blog-v1
from flask import Blueprint, render_template

from blogDog.visualData.visualData import chartList, chartFile

visual_bp = Blueprint('visual', __name__)


@visual_bp.route('/list', methods=['GET'])
def index():
    return render_template('visual/index.html')


@visual_bp.route('/list/<chart_name>', methods=['GET', 'POST'])
def show_chart(chart_name):
    if not chart_name:
        chart_name = '3d-earth'
    requireFiles = chartFile[chart_name]
    return render_template('visual/index.html', requireFiles=requireFiles)


@visual_bp.context_processor
def add_template_processor():
    return dict(chartList=chartList)
