# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1
import re
from datetime import datetime

from flask_login import UserMixin
from jinja2.filters import do_truncate, do_striptags
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash

from blogDog.extensions import db

pattern_hasmore = re.compile(r"<!--more-->", re.I)


def markitup(text):
    # 将 markdown 转为 HTML

    # 删除与段落相关的标签，只留下格式化字符的标签
    # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
    #                 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    #                 'h1', 'h2', 'h3', 'p', 'img']
    return markdown(text, extensions=['extra'], output_format='html5')
    # return bleach.linkify(markdown(text, extensions=['extra'], output_format='html5'))
    # return bleach.linkify(bleach.clean(
    #     # markdown默认不识别三个反引号的code-block，需开启扩展
    #     markdown(text, extensions=['extra'], output_format='html5'),
    #     tags=allowed_tags, strip=True))


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Admin.{self.username}"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    isSubject = db.Column(db.Boolean, default=False)
    subject_info = db.Column(db.Text)  # 添加备注信息

    # 一对多
    posts = db.relationship("Post", back_populates="category")

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]  # todo ??
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

    @property
    def getPostNum(self):
        num = 0
        for post in self.posts:
            if post.published:
                num += 1
        return num


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    sub_title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    can_comment = db.Column(db.Boolean, default=True)
    isRecommend = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=True)  # 是否发布文章

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship("Category", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    @staticmethod
    def before_insert(mapper, connection, target):
        def _format(_html):
            return do_truncate(do_striptags(_html), True, length=150)

        value = target.body
        # print('value =============', value)
        if target.sub_title is None or target.sub_title.strip() == '':
            _match = pattern_hasmore.search(value)
            if _match is not None:
                more_start = _match.start()
                # print(more_start)
                target.sub_title = _format(markitup(value[:more_start]))
            else:
                target.sub_title = _format(target.body_html)

    @staticmethod
    def on_change_content(target, value, oldvalue, initiator):
        # print(value, '========================= value')
        target.body_html = markitup(value)
        # print(target.body_html)

        def _format(_html):
            return do_truncate(do_striptags(_html), True, length=150)

        if target.sub_title is None or target.sub_title.strip() == '':
            _match = pattern_hasmore.search(value)
            if _match is not None:
                more_start = _match.start()
                target.summary = _format(markitup(value[:more_start]))
                # target.sub_title = markitup(value[:more_start])
            else:
                target.summary = target.body_html
                # target.sub_title = _format(target.body_html)


# 事件监听
db.event.listen(Post.body, 'set', Post.on_change_content)
db.event.listen(Post, 'before_insert', Post.before_insert)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255), default='')
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    message = db.Column(db.Text, default='')  # 添加备注信息
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
