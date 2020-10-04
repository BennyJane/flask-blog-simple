# -*- coding: utf-8 -*-
# @Time : 2020/10/2
# @Author : Benny Jane
# @Email : 暂无
# @File : forms.py
# @Project : flask-blog-v1
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, URL, Email
from datetime import date
from blogDog import Category


class LoginForm(FlaskForm):
    username = StringField('名称', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('remember me')
    # todo  自定义表单字段的 类， 失效 => {"class": "btn-sm"}
    submit = SubmitField('登录', render_kw={'style': 'background-color: black; color: white'})


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(u"不能为空"), Length(1, 100)])
    sub_title = TextAreaField("简介", validators=[DataRequired(), Length(1, 500)])
    # todo ?
    category = SelectField("分类", coerce=int, default=1)
    can_comment = BooleanField("是否可以评论", default=True)
    isRecommend = BooleanField("是否推荐该文章", default=False)
    body = CKEditorField('正文', validators=[DataRequired()])
    submit = SubmitField("提交", render_kw={'style': 'background-color: black; color: white'})

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(1, 100)])
    isSubject = BooleanField('是否是专题文章', default=False)
    subject_info = TextAreaField("分类或者专题文章的简介", default='')
    submit = SubmitField("提交", render_kw={'style': 'background-color: black; color: white'})


class LinkForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 100)])
    # url = TextAreaField('网址', validators=[URL()], default='')
    message = TextAreaField("简介", default='')
    timestamp = StringField("日期", default=date.today().isoformat())
    url = TextAreaField('网址', validators=[], default='')
    submit = SubmitField("提交", render_kw={'style': 'background-color: black; color: white'})


class CommentForm(FlaskForm):
    author = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    # site = db.Column(db.String(255), default='')
    body = TextAreaField("评论", validators=[DataRequired()])
    submit = SubmitField("提交", render_kw={'style': 'background-color: black; color: white'})


class AdminCommentForm(CommentForm):
    # 继承评论类
    author = HiddenField()
    email = HiddenField()
