from . import auth_bp
from flask.views import MethodView
from flask import render_template,request
from .forms import LoginForm,RegisterForm
from .models import User
from flask_login import login_user
from app import db

# 登陆
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

        return render_template("auth/register.html",form=self.form)