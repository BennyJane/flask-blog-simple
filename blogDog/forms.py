# -*- coding: utf-8 -*-
# @Time : 2020/10/2
# @Author : Benny Jane
# @Email : 暂无
# @File : forms.py
# @Project : flask-blog-v1
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('名称', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('remember me')
    # todo  自定义表单字段的 类， 失效 => {"class": "btn-sm"}
    submit = SubmitField('登录', render_kw={'style': 'background-color: black; color: white'})
