# -*- coding: utf-8 -*-
# @Time : 2020/10/3
# @Author : Benny Jane
# @Email : 暂无
# @File : email.py
# @Project : flask-blog-v1
from threading import Thread

from flask import current_app, url_for
from flask_mail import Message

from blogDog.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message=message)


def send_mail(subject, to, html):
    app = current_app._get_current_object()
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    html = f'''
    <h2>文章《{post.title}》新增一条评论</h2>
    <p>点击下面链接，查看评论的文章</p>
    <p><a>{post_url}</a></p>
    <p><small style="color: #868e96">Do not reply this email.</small></p>
    '''
    send_mail(subject="新增评论", to=current_app.config['BLOGDOG_EMAIL'],
              html=html
              )


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    html = f'''
    <h2>你在文章《{comment.post.title}》下的评论收到了一条回复</h2>
    <p>点击下面链接，查看评论的文章</p>
    <p><a>{post_url}</a></p>
    <p><small style="color: #868e96">Do not reply this email.</small></p>
    '''
    send_mail(subject="新增回复", to=comment.email,
              html=html
              )
