from . import auth_bp
from .views import Login,Register,Confirm,Unconfirm,ResetPasswd,ForgetPassword,ForgetResetPassword,ResendEmail

auth_bp.add_url_rule("/login",view_func=Login.as_view("login"))
auth_bp.add_url_rule("/register",view_func=Register.as_view("register"))
auth_bp.add_url_rule("/confirm/<token>",view_func=Confirm.as_view("confirm"))
auth_bp.add_url_rule("/unconfirm",view_func=Unconfirm.as_view("unconfirm"))
auth_bp.add_url_rule("/resetPasswd",view_func=ResetPasswd.as_view("resetPasswd"))
auth_bp.add_url_rule("/forgetPassword",view_func=ForgetPassword.as_view("forgetPassword"))
auth_bp.add_url_rule("/resendEmail",view_func=ResendEmail.as_view("resendEmail"))
auth_bp.add_url_rule("/forgetResetPassword/<token>",view_func=ForgetResetPassword.as_view("forgetResetPassword"))



