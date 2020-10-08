# -*- coding: utf-8 -*-
# @Time : 2020/10/4
# @Author : Benny Jane
# @Email : 暂无
# @File : log.py
# @Project : flask-blog-v1
import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import request

basedir = os.path.abspath(os.path.dirname(__file__))


def register_logging(app):
    # todo 自定义日志信息类，添加信息的日志信息
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%s(asctime)s] %s(remote_addr)s requested %s(url)s %(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)S - %(name)S - %(levelname)S -%(message)S')
    # 判断该目录是否存在
    logPath = os.path.join(basedir, 'logs')
    if not os.path.exists(logPath):
        os.mkdir(logPath)

    # 文件日志处理
    # 日志文件保存路径； 单个日志文件最大尺寸； 备份文件数量， 超过后覆盖之前的文件
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/blogdog.log'), maxBytes=10 * 1024 * 1204,
                                       backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    # 邮件日志处理
    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=app.config['BLOGDOG_EMAIL'],
        subject='blogDog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    )
    mail_handler.setLevel(logging.INFO)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:  # todo app.debug判断当前是否在调试模式
        # 非调试模式下，开启日志功能
        # todo 将处理器注册到龙个人对象中
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)
