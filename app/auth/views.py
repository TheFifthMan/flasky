# coding: utf-8 
from auth import auth_bp
from flask.views import MethodView
from flask import render_template,flash,redirect,url_for,request
from flask_login import login_user,url_for,redirect
from .forms import RegisterForm, \
                    LoginForm, \
                    ResetPasswdForm, \
                    ForgetPasswordForm, \
                    ResetForgetPasswordForm

# 注册
def Register(MethodView):
    def __init__(self,**kw):
        super(Register,self).__init__(**kw)
        self.form = RegisterForm()

    def get(self):
        return render_template("auth/register.html",title="Register",form=self.form)

    def post(self):
        

# 已确认注册信息
class Comfirm(MethodView):
    def get(self):
        pass

# 未确认注册邮箱
class Unconfirm(MethodView):
    def get(self):
        pass

# 重新发送密码
class ResendEmail(MethodView):
    def post(self):
        pass

# 登陆
class Login(MethodView):
    def __init__(self,**kw):
        super(Login,self).__init__(**kw)
        self.form = LoginForm()

    def get(self):
        return render_template("auth/register.html",title="Register",form=self.form)
    
    def post(self):
        if self.form.validate_on_submit():
            email = self.form.email.data
            user = User.query.filter_by(email=email).first()
            if user is not None and user.verify_password(self.form.password.data):
                login_user(user)
                flash("Login Succeed!")
                next = request.args.get("next")
                if next is None or not next.startwith("/"):
                    next = url_for('index.index')
                
                return redirect(next)
        flash("invlida username or password")
        return render_template("auth/login.html",title="Login",form=self.form)

# 退出登陆
class Logout(MethodView):
    def get(self):
        pass

# 重置密码
def ResetPasswd(MethodView):
    def __init__(self,**kw):
        super(ResetPasswd,self).__init__(**kw)
        self.form = ResetPasswdForm()

    def get(self):
        pass
    
    def post(self):
        pass

# 忘记密码，需要填写邮箱信息，用于发送链接用于重置密码请求
class ForgetPasswd(MethodView):
    def __init__(self,**kw):
        super(ForgetPasswd,self).__init__(**kw)
        self.form = ForgetPasswordForm()

    def get(self):
        pass
    
    def post(self):
        pass

# 忘记密码，重置密码模块
class ResetForgetPasswd(MethodView):
    def __init__(self,**kw):
        super(ResetForgetPasswd,self).__init__(**kw)
        self.form = ResetForgetPasswordForm()

    def get(self):
        pass
    
    def post(self):
        pass


