from . import auth_bp
from .views import  Register, \
                    Login, \
                    ResetPasswd, \
                    ForgetPasswd, \
                    ResetForgetPasswd, \
                    Comfirm, \
                    Unconfirm, \
                    ResendEmail

auth_bp.add_url_rule('/register',view_func=Register.as_view("register"))
auth_bp.add_url_rule('/login',view_func=Login.as_view("login"))
auth_bp.add_url_rule('/reset_passwd',view_func=ResetPasswd.as_view("reset_passwd"))
auth_bp.add_url_rule('/forget_passwd',view_func=ForgetPasswd.as_view("forget_passwd"))
auth_bp.add_url_rule('/reset_forget_passwd',view_func=ResetForgetPasswd.as_view("reset_forget_passwd"))
auth_bp.add_url_rule('/confirm/<token>',view_func=Comfirm.as_view("confirm"))
auth_bp.add_url_rule('/unconfirm',view_func=Uncomfirm.as_view("unconfirm"))
auth_bp.add_url_rule('/resend_email',view_func=ResendEmail.as_view("resend_email"))







