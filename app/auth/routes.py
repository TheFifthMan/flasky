from . import auth_bp
from .views import Login,Register

auth_bp.add_url_rule("/login",view_func=Login.as_view("login"))
auth_bp.add_url_rule("/register",view_func=Register.as_view("register"))
