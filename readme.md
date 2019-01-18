# session 管理 + 登陆 + 注册 + 忘记密码 
## session管理
flask可以使用flask-login 来做session管理，先配置好 flask-login
```
pipenv install flask-login 
```
然后在app 实例中初始化
```py
# app/__init__.py
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
def create_app(config_name):
    ...
    # 初始化各种插件
    ...
    login_manager.init_app(app)
    ...
```
对数据库对象进行绑定
```py
# app/auth/models.py
from flask_login import UserMixin
from app import login_manager
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = "users"
    ...
```
User绑定了一个UserMixin对象，每次session都会来这里load user

# 登陆
登陆有4个步骤
1. 表单对象
2. 模板设置
3. 逻辑处理
4. 加入路由

## 表单对象
```py
# app/auth/forms.py
from flask-wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Keep me Logged in")
    submit = SubmitField("Log In")
```
## 模板设置
模板设置大多使用到 html 和 css 的知识，就不多赘述了
```html
# templates/base.html
{% extends "bootstrap/base.html" %}

{% block title %}Flasky{% endblock %}

{% block head %}
{{ super() }}
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}" type="image/x-icon">
<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
{% endblock %}

{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle"
             data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Flasky</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                {% if current_user.is_authenticated %}
                <li><a href="{{ url_for('auth.logout') }}">Log Out</a></li>
                {% else %}
                <li><a href="{{ url_for('auth.login') }}">Log In</a></li>
                {% endif %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}
{% block content %}
<div class="container">
    {% block page_content %}{% endblock %}
</div>
{% endblock %}

{% block scripts %}
{{ super() }}
{% endblock %}


# templates/auth/login.html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky - Login{% endblock %}

{% block page_content %}
    <div class="page-header">
    <h1>Login</h1>
    </div>
    <div class="col-md-4">
        {{ wtf.quick_form(form) }}
    </div>
{% endblock %}
```
## 逻辑处理
```py
from . import auth_bp
from flask.views import MethodView
from flask import render_template,request
from .forms import LoginForm
from .models import User
from flask_login import login_user
class Login(MethodView):
    def __init__(self,**kw):
        super(Login,self).__init__(**kw)
        self.form = LoginForm()
        
    def get(self):
        return render_template("auth/login.html",form=self.form)

    def post(self):
        if self.form.validate_on_submit():
            user = User.query.filter_by(self.form.email.data).first()
            if user is not None and user.verify_password(self.form.password.data):
                login_user(user,form.remember_me.data)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('index.index')
                return redirect(next)
        
        return render_template("auth/login.html",form=self.form)
```
## 加入路由
```py
auth_bp.add_url_rule("/login",view_func=Login.as_view("login"))
```

# 注册
注册也是同样4步,不过最后要加一个邮件确认注册的过程
## 表单对象
```py
class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    password1 = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password Confirm",validators=[DataRequired(),EqualTo('password1')])    
    submit = SubmitField("Register")

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email registered")
    
    def validate_name(self,filed):
        if User.query.filter_by(name=filed.data).first():
            raise ValidationError("name registered")
```
## 模板设置
```py
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky - Login{% endblock %}

{% block page_content %}
    <div class="page-header">
    <h1>Register</h1>
    </div>
    <div class="col-md-4">
        {{ wtf.quick_form(form) }}
    </div>
{% endblock %}
```

## 逻辑处理
```py
class Register(MethodView):
    def __init__(self,**kw):
        super(Register,self).__init__(**kw)
        self.form = RegisterForm()
    
    def get(self):
        return render_template("auth/register.html",form=self.form)
    
    def post(self):
        if self.form.validate_on_submit():
            user = User(username=self.form.name.data,password=self.form.password1.data,email=self.form.email.data)
            db.session.add(user)
            db.session.commit()

        return render_template("auth/register.html",form=self.form)
```
## 加入路由
```
auth_bp.add_url_rule("/register",view_func=Register.as_view("register"))
```
现在已经可以访问 register 了，也可以把用户加入数据库了，但是还需要一个用户邮件确认注册的操作. 
```py
# app/auth/views.py
# 注册
class Register(MethodView):
    def __init__(self,**kw):
        super(Register,self).__init__(**kw)
        self.form = RegisterForm()
    
    def get(self):
        return render_template("auth/register.html",form=self.form)
    
    def post(self):
        if self.form.validate_on_submit():
            user = User(username=self.form.name.data,password=self.form.password1.data,email=self.form.email.data)
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.id)
            send_email(user.email,"Confirm Your Account","auth/email/confirm",user=user,token=token)
            flash("Please confirm your email account!")
            return redirect("auth.unconfirm")

        return render_template("auth/register.html",form=self.form)
```



# 忘记密码
忘记密码就不能使用上面的token 来作为验证用户的手段，首先分析一下逻辑
1. 用户点击忘记密码，填写邮箱
2. 系统发送一个链接到用户的邮箱
3. 用户打开自己的邮箱点击里面的链接
4. 打开了重置密码的页面，填写新密码



# 测试
当完成一个功能以后，需要做好质量保障：
1. 写好单元测试
2. 写好功能测试

这里因为还没有API，所以功能测试只测试UI，使用selenium 作为驱动

 