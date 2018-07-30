## flask基础
### 1. 倚赖的环境
- **导入SQLAlchemy操作数据库** `pip install -i https://pypi.douban.com/simple flask-sqlalchemy`
- **查看ip** `ifconfig`
- **查看端口** `show global variables like 'port';`
- **flask配置mysql**
```python
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/flaskMovies"
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

db = SQLAlchemy(app)
```
- **打开视屏文件** `smplayer xxx.mp4`
- **查看倚赖的环境** `pip list`
- **导入pymysql** `pip install -i https://pypi.douban.com/simple pymysql`
- **切换数据库** `use flaskMovies;`
- **查看数据库表** `show tables;`
- **查看表结构也** `desc movie;`

### 2. 命令行操作
- **查看版本** `flask --version`
### 3. Flask构建微电影网站
#### 3.3 创建数据模型
***
- **往role表中插入超级管理员**
```python
# 路径 /1-flask_movie/app/models.py
# 插入超级管理员字段
    role = Role(
        name='超级管理员',
        auths=''
    )
    db.session.add(role)
    db.session.commit()
```
- **报错数据库编码问题,设置为urf8mb4**
> sqlalchemy.exc.InternalError: (pymysql.err.InternalError) (1366, "Incorrect string value: '\\xE7\\xAE\\xA1\\xE7\\x90\\x86...' for column 'name' at row 1")<br>
- **解决方案<br>**
**https://mathiasbynens.be/notes/mysql-utf8mb4**
```
ALTER DATABASE flaskMovies CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE role CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
***
- **插入管理员字段,并使用哈希盐加密**
```python
from werkzeug.security import generate_password_hash
admin = Admin(
    name='imoocmovie',
    pwd=generate_password_hash('imoocmovie'),
    is_supper=0,
    role_id=1
)
db.session.add(admin)
db.session.commit()
```
- **查询出的结果按列显示**
> mysql> select * from admin\G;<br>
*************************** 1. row ***************************<br>
id: 1<br>
name: imoocmovie<br>
pwd: pbkdf2:sha256:50000$min7c0if$76354f589b8113ae9bb7aa2f9bad1d09c202ba066b50d8408f7e889898412d77<br>
is_supper: 0<br>
role_id: 1<br>
addtime: 2018-07-25 04:52:54
***
#### 3.4 搭建前台页面
- **前台页面搭建**
    1. 静态文件引入: `{{ url_for('static', filename='文件路径') }}`
    2. 定义路由: `{{ url_for('模块名.视图名', 变量=参数) }}`
    3. 定义数据块: `{% block 数据块名称 %}`...`{% endblock %}`
***
- **电影详情页面的搭建**
```python
# 路径 /1-flask_movie/home/views
@home.route('/play/')
def paly():
    return render_template('home/play.html')
```
```
<!--继承父模板-->
{# 路径 /1-flask_movie/templates/home/play.html #}
{% extends 'home/home.html' %}

{% block css %}
{% endblock %}

{% block content %}
{% endblock %}
```
***
- **404页面的搭建**<br>
```不在蓝图模块里面定义,而是在初始化文件里定义```
```Python
# 路径 /1-flask_movie/home/__init__.py
from flask import Flask, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
```
#### 3.5 搭建后台页面

- **管理员登录页面的搭建**
```
# 登录 /1-flask_movie/app/admin/views.py
@admin.route('/login/')
def login():
    return render_template('admin/login.html')


# 退出
@admin.route('/logout/')
def logout():
    return redirect(url_for('admin.login'))
```
***
- **测试url是否通路**
```
# 路径 /1-flask_movie/app/admin/views.py
@admin.route('/')
def index():
    return "<h1 style='color:red'>this is admin</h1>"
```
***
- **后台布局搭建**<br>
`惯用的一个套路,使用extends把母版继承过来,再用数据块block进行添加内容`

```python
# 母版 /1-flask_movie/app/admin/templates/admin.html
{% block css %}...{% endblock %}
{% include 'grid.html' %}
{% block content %}...{% endblock %}
{% block js %}...{% endblock %}

# 其他页面继承父模板
{% extends 'admin/admin.html' %}
{% block css %}...{% endblock %}
{% include 'grid.html' %}
{% block content %}...{% endblock %}
{% block js %}...{% endblock %}
```
***
- **修改密码页面搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
@admin.route('/pwd/')
def pwd():
    return render_template('admin/pwd.html')
```
***
- **控制面板页面的搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
@admin.route('/')
def index():
    return render_template('admin/index.html')
```
- 内存使用率可视化<br>
`通过block数据块,添加echarts.min.js插件`
```html
# 路径 /1-flask_movie/app/templates/admin/index.html
{% block js %}
    <script src="{{ url_for('static', filename='base/js/echarts.min.js') }}"></script>
    <script>
        var myChart = echarts.init(document.getElementById('meminfo'));
        option = {
            backgroundColor: "white",
            tooltip: {
                formatter: "{a} <br/>{b} : {c}%"
            },
            toolbox: {
                feature: {
                    restore: {},
                    saveAsImage: {}
                }
            },
            series: [{
                name: '内存使用率',
                type: 'gauge',
                detail: {
                    formatter: '{value}%'
                },
                data: [{
                    value: 50,
                    name: '内存使用率'
                }]
            }]
        };
        setInterval(function () {
            option.series[0].data[0].value = (Math.random() * 100).toFixed(2) - 0;
            myChart.setOption(option, true);
        }, 2000);

    </script>
{% endblock %}
```
- 自动打开列表
```html
# 路径 /1-flask_movie/app/templates/admin/index.html
<script>
        $(document).ready(function(){
            $("#g-1").addClass("active");
            $("#g-1-1").addClass("active");
        });
</script>
```
***
- **标签管理页面的搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
# 编辑标签 
@admin.route('/tag/add/')
def tag_add():
    return render_template('admin/tag_add.html')
    
# 标签列表
@admin.route('/tag/list/')
def tag_list():
    return render_template('admin/tag_list.html')
```
- 模板语言生成十次
```html
# 路径 /1-flask_movieapp/app/templates/admin/tag_list.html
{% for v in range(0,10) %}
<tr>
    <td>1</td>
    <td>科幻</td>
    <td>2017-06-01</td>
    <td>
        <a class="label label-success">编辑</a>
        &nbsp;
        <a class="label label-danger">删除</a>
    </td>
</tr>
{% endfor %}
```
> 这里有两种分隔符: {% ... %} 和 {{ ... }} 。前者用于执行诸如 for 循环 或赋值的语句，后者把表达式的结果打印到模板上。
***
- **电影管理页面搭建**
```python
# 编辑电影
# 路径 /1-flask_movie/app/admin/views.py
@admin.route('/movie/add/')
def movie_add():
    return render_template('admin/movie_add.html')
    
# 电影列表
@admin.route('/movie/list/')
def movie_list():
    return render_template('admin/movie_list.html')
```
***
- **上映预告管理页面搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
# 编辑上映预告
@admin.route('/preview/add/')
def preview_add():
    return render_template('admin/preview_add.html')
    
# 上映预告列表
@admin.route('/preview/list/')
def preview_list():
    return render_template('admin/preview_list.html')
```
***
- **会员管理页面搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
# 会员列表
@admin.route('/user/list/')
def user_list():
    return render_template('admin/user_list.html')
    
# 查看会员
@admin.route('/user/view/')
def user_view():
    return render_template('admin/user_view.html')
```
***
- **评论管理页面的搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
# 评论列表
@admin.route('/comment/list/')
def comment_lsit():
    return render_template('admin/comment_list.html')
```
***
- **收藏管理页面搭建**
```python
# 路径 /1-flask_movie/app/admin/views.py
# 收藏列表
@admin.route('/moviecol/list/')
def moviecol_list():
    return render_template('admin/moviecol_list.html')
```
***
- **日志管理页面搭建**<br>
- <font size=2>操作管理页面搭建</font>
```python
# 路径 /1-flask_movie/app/admin/views.py
# 操作日志列表
@admin.route('/oplog/list/')
def oplog_list():
    return render_template('admin/oplog_list.html')
```
- <font size=2></font>

