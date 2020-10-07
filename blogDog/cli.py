# -*- coding: utf-8 -*-
# @Time : 2020/10/1
# @Author : Benny Jane
# @Email : 暂无
# @File : __init__.py
# @Project : flask-blog-v1
import click

from blogDog.fakes import fake_admin
from blogDog.models import Admin, Category

'''
这一部分可以直接写在 __init__.py 文件内， 不用传入db， 直接使用__init__.py 中引入的db全局变量
'''


# todo 在该文件中直接引入db，会报错； ==》 ？？ db还没有绑定
# todo db已经在__init__.py 文件中被引入了
def command1(app, db):
    # 初始化数据库
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            # todo ??
            click.confirm("This operation will delete the database, do you want to continue?", abort=True)
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialize database.")


def command2(app, db):
    # todo prompt ? 必须输入该参数
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo("该账号已经存在，更新密码.")
            admin.username = username
            admin.set_password(password)
        else:
            click.echo("创建管理员账号")
            admin = Admin(
                username=username,
                blog_title="A Dog",
                blog_sub_title="This is the life!",
                name="Admin",
                about="There is nothing!",
            )
            admin.set_password(password)
        db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo("添加默认分类")
            category = Category(name="Default")
            db.session.add(category)
        db.session.commit()
        click.echo('Done.')


def command3(app, db):
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    @click.option('--recommend', default=10, help='Quantity of recommend, default is 10')
    @click.option('--subject', default=3, help='Quantity of subject, default is 3')
    def forge(category, post, comment, recommend, subject):
        """Generate fake data."""
        from blogDog.fakes import fake_categories, fake_posts, fake_comments, fake_links, fake_subject, \
            fake_recommend_post

        # todo 为什么要执行这一步??
        db.drop_all()
        db.create_all()

        click.echo("Generating %d categories ..." % category)
        fake_categories(category)

        click.echo("Generating %d post ..." % post)
        fake_posts(post)

        click.echo("Generating %d comment ..." % comment)
        fake_comments(comment)

        click.echo("Generating %d recommend ..." % recommend)
        fake_recommend_post(recommend)

        click.echo("Generating %d subject ..." % subject)
        fake_subject(subject)

        click.echo('Generating links...')
        fake_links()

        click.echo("Generating admin: (benny blogdog)")
        fake_admin()

        click.echo('Done.')
