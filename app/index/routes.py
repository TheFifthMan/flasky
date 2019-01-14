from . import index_bp
from .views import Index

index_bp.add_url_rule('/',view_func=Index.as_view('index'))


# 当需要url_for 的时候，可以使用 index 这个名字 index.index
# url_for('index.index') index 可以类比为就是这个函数的名字