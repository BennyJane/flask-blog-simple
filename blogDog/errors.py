# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1
from flask import render_template


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errros/400.html"), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500
