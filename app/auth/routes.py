from . import auth_bp
from .views import Login,Register,Confirm,Unconfirm,ResetPasswd,ForgetPassword,ForgetResetPassword,ResendEmail

auth_bp.add_url_rule("/Login",view_func=Login.as_view("Login"))
auth_bp.add_url_rule("/Register",view_func=Register.as_view("Register"))
auth_bp.add_url_rule("/Confirm/<token>",view_func=Confirm.as_view("Confirm"))
auth_bp.add_url_rule("/Unconfirm",view_func=Unconfirm.as_view("Unconfirm"))
auth_bp.add_url_rule("/ResetPasswd",view_func=ResetPasswd.as_view("ResetPasswd"))
auth_bp.add_url_rule("/ForgetPassword",view_func=ForgetPassword.as_view("ForgetPassword"))
auth_bp.add_url_rule("/ResendEmail",view_func=ResendEmail.as_view("ResendEmail"))
auth_bp.add_url_rule("/ForgetResetPassword/<token>",view_func=ForgetResetPassword.as_view("ForgetResetPassword"))



