from . import auth_bp
from flask.views import MethodView
from flask import render_template,request,redirect,flash,url_for,abort
from .forms import LoginForm,RegisterForm
from .models import User
from flask_login import login_user,current_user,login_required
from app import db
from app.utils.encrypt import encrypt_forget_passwd_token,verify_forget_passwd_token,generate_confirmation_token,confirm

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
            token = generate_confirmation_token(user.id)
            send_email(user.email,"Confirm Your Account","auth/email/confirm",user=user,token=token)
            flash("Please confirm your email account!")
            return redirect("auth.unconfirm")

        return render_template("auth/register.html",form=self.form)


class Confirm(MethodView):
    def get(self,token):
        if confirm(token):
            flash("You have Confirmed your email!")
        else:
            flash("Error")
        return redirect("index.index")


class Unconfirm(MethodView):
    def get(self):
        if current_user.is_anonymous or current_user.confirmed:
            return redirect("index.index")
        return render_template("auth/unconfirmed.html")


class ResetPasswd(MethodView):
    def __init__(self,**kw):
        super(ResetPasswd,self).__init__(**kw)
        self.form = ResetPasswdForm()

    @login_required
    def get(self):
        return render_template("auth/resetpasswd.html",form=self.form)

    @login_required
    def post(self):
        if self.form.validate_on_submit():
            if current_user.verify_password(self.form.password.data):
                current_user.password = self.form.newpassword.data
                flash("Changed your password")
                db.session.commit()
                return redirect("auth.login")
            else:
                flash("Your password is uncorrect!")
                return redirect("auth.reset_passwd")


class ForgetPassword(MethodView):
    def __init__(self,**kw):
        super(ForgetPassword,self).__init__(**kw)
        self.form = ForgetPasswordForm()
    
    def get(self):
        if current_user.is_authenticated:
            return redirect("index.index")
        
        return render_template("auth/forget.html",form=self.form)
    
    def post(self):
        if self.form.validate_on_submit():
            email = self.form.email.data
            u = User.query.filter_by(email=email).first()
            if u is not None:
                token = u.generate_confirmation_token()
                send_email(user.email,"Reset Your Password","auth/email/forget",user=user,token=token)
                flash(" send email succeed!")
            else:
                flash("user not exists")
        
            return redirect("auth.login")


class ForgetResetPassword(MethodView):
    def __init__(self,**kw):
        super(ForgetResetPassword,self).__init__(**kw)
        self.form = ForgetResetPasswordForm()

    def get(self,token):
        if verify_forget_passwd_token(token):
            return render_template("auth/forget_reset_password.html",self.form = form)
        else:
            abort(404)
    
    def post(self,token):
        if self.form.validate_on_submit():
            if reset_passwd(token,self.form.password):
                flash("reset password succeed! please login")
                return redirect("auth.login")
            else:
                flash("Reset password failed")
                return redirect("auth.forget_password")


class ResendEmail(MethodView):
    @login_required
    def get(self):
        token = current_user.generate_confirmation_token()
        send_email(current_user.email,"Confirm Your Account","auth/email/confirm",user=current_user,token=token)
        flash("send succeed!")
        return url_for("index.index")


@auth_bp.before_request
def before_request():
    if not current_user.confirmed \
        and request.blueprint != "auth" \
        and request.endpoint != "static":
        return redirect("auth.unconfirm")
                
