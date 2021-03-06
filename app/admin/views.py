import math
from contextlib import contextmanager

from flask import render_template, redirect, url_for, flash, session, request, appcontext_pushed

from app import db
from app.admin.forms import LoginForm, TagForm
from app.models import Admin, Tag
from . import admin
from functools import wraps

"""
使用session做一个访问控制:
使用装饰器简化视图函数代码
flask采用线程隔离的思想,每次创建线程都使用上下文技术为该线程创建一个对应的全局的http对象,
随着线程的结束,该对象的生命周期也会结束,存放的栈会被释放
def admin_login_req(func):
    with app.test_request_context():
        @wraps(func)
        def decorated_function():
            if 'admin' not in session:
                return redirect(url_for('admin.login'))
            else:
                func()

        return decorated_function()
"""


@admin.route('/')
# @admin_login_req
def index():
    if 'admin' not in session:
        return redirect(url_for('admin.login', next=request.url))
    else:
        return render_template('admin/index.html')


# 登录
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash('密码错误!', 'err')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


# 退出
@admin.route('/logout/')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route('/pwd/')
def pwd():
    return render_template('admin/pwd.html')


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
def tag_add():
    if 'admin' not in session:
        return redirect(url_for('admin.login', next=request.url))
    else:
        form = TagForm()
        if form.validate_on_submit():
            data = form.data
            name = data['name']
            tag = Tag.query.filter_by(name=name).count()
            if tag >= 1:
                flash('名称已经存在!', 'err')
                return redirect(url_for('admin.tag_add'))
            tag = Tag(
                name=data['name']
            )
            db.session.add(tag)
            db.session.commit()
            flash('添加标签成功!', 'ok')
            return redirect(url_for('admin.tag_add'))
        return render_template('admin/tag_add.html', form=form)


# 标签列表
@admin.route('/tag/list/<int:page>/<int:per_page>/', methods=['GET'])
def tag_list(page=None, per_page=None):
    if 'admin' not in session:
        return redirect(url_for('admin.login', next=request.url))
    else:
        if (page or per_page) is None:
            page = 1
            per_page = 5
        page_data = Tag.query.order_by(
            Tag.add_time.asc()
        ).paginate(page=page, per_page=per_page, error_out=True)
        # 测试
        # list = []
        # pages = page_data.iter_pages()
        # for page in pages:
        #     list.append(page)
        return render_template('admin/tag_list.html', page_data=page_data)


# 编辑电影
@admin.route('/movie/add/')
def movie_add():
    return render_template('admin/movie_add.html')


# 电影列表
@admin.route('/movie/list/')
def movie_list():
    return render_template('admin/movie_list.html')


# 编辑上映预告
@admin.route('/preview/add/')
def preview_add():
    return render_template('admin/preview_add.html')


# 上映预告列表
@admin.route('/preview/list/')
def preview_list():
    return render_template('admin/preview_list.html')


# 会员列表
@admin.route('/user/list/')
def user_list():
    return render_template('admin/user_list.html')


# 查看会员
@admin.route('/user/view/')
def user_view():
    return render_template('admin/user_view.html')


# 评论列表
@admin.route('/comment/list/')
def comment_list():
    return render_template('admin/comment_list.html')


# 收藏列表
@admin.route('/moviecol/list/')
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 操作日志列表
@admin.route('/oplog/list/')
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员日志列表
@admin.route('/adminloginlog/list/')
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员日志列表
@admin.route('/userloginlog/list/')
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 添加权限
@admin.route('/auth/add/')
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admin.route('/auth/list/')
def auth_list():
    return render_template('admin/auth_list.html')


# 添加角色
@admin.route('/role/add/')
def role_add():
    return render_template('admin/role_add.html')


# 添加列表
@admin.route('/role/list/')
def role_list():
    return render_template('admin/role_list.html')


# 添加管理员
@admin.route('/admin/add/')
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route('/admin/list/')
def admin_list():
    return render_template('admin/admin_list.html')
