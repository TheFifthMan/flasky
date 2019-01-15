# 认证管理 + 权限分配 初始化

# 认证管理
## 新建数据库
```
create database `flasky` default character set utf8 collate utf8_general_ci;
```
## 需要的插件
```
flask-mail: 用来发送认证信息
flask-login: 用于管理session
werzeug+itsdangerous：用于密码hash加盐
flask-wtf：表单对象创建
flask-bootstrap： bootstrap 渲染
```
## 建立认证蓝图
```py
# auth/__init__.py
# coding: utf-8 
from flask import Blueprint
auth_bp = Blueprint("/",__name__)
from . import views,routes,models

# app/__init__.py
def create_app(config_name):
    ...
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
```
## 建立用户ORM模型
```py
# auth/models.py
# coding: utf-8 
from werkzeug.security import generate_password_hash,check_password_hash
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    
    @property
    def password(self):
        raise AttributeError("password is not readable attribute")
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
```

# 权限分配
## 权限等级设置
name | permission name | permission value
-----|-----------------|-------------------
Follow users | FOLLOW | 1
Comment on posts made by others| COMMENT | 2
Write articles | WRITE | 4
Moderate comments | MODERATE | 8 
Admin | ADMIN | 16 

直接新建一个 Permission 对象来表示权限
```py
# auth/models.py
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16
```
设置三种用户角色
角色|权限|描述
---|---|---
None | None | 只读
User | FOLLOW/COMMENT/WRITE| 基础权限
Moderator| FOLLOW/COMMENT/WRITE/MODERATOR| 多一个修改评论权限
ADMIN|FOLLOW/COMMENT/WRITE/MODERATOR/ADMIN| 多一个管理员权限

## 建立角色模型
```py
# auth/models.py
# coding: utf-8 
from werkzeug.security import generate_password_hash,check_password_hash
from app import db

class Role(db.Model):
    __tablename__ == "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))
    default = db.Column(db.Boolean,default=False,index=True) # 只设置给一个用户，其他用户都是False，因为app 会去搜索这个值，因此设置为 index 方便查找
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self,**kw):
        super(Role,self).__init__(**kw)
        if self.permissions is None:
            self.permissions = 0

    # 判断是否含有权限  
    def has_permission(self,perm):
        return self.permissions & perm == perm

    # 添加权限
    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions += perm
    # 移除权限
    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # 重置权限
    def reset_permission(self,perm):
        self.permissions = 0    
    
    # 插入角色
    # 插入角色
    @staticmethod
    def insert_roles():
        roles = {
            "User":[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
            ],
            "Moderator":[
                Permission.MODERATE
            ],
            "ADMIN":[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,  
                Permission.ADMIN,          
            ]
        }
        # 默认角色是用户
        default_role = 'User'
        for r in roles:
            # 搜索三种角色，在数据库表的存在
            role = Role.query.filter_by(name=r).first()
            # 如果不存在这种角色，马上添加进去，方便以后拓展
            if role is None:
                role = Role(name=r)
            
            # 重置权限
            role.reset_permission()
            for perm in roles[r]:
                # 权限重新一个个加进去
                role.add_permission(perm)
            
            # 将默认用户写进数据库
            role.default = (role.name == default_role)
            db.session.add(role)
        
        db.session.commit()
```
然后是分配角色给用户
```py
# app/auth/models.py
class User(db.Model):
    def __init__(self,**kw):
    
        super(User,self).__init__(**kw)
        # 分配管理员角色
        if self.role is None and self.email == current_app.config['FLASKY_ADMIN']:
            self.role = Role.query.filter_by(name="ADMIN").first()

        # 如果一个用户的角色不存在
        if self.role is None:
            # 分配一个默认角色
            self.role = Role.query.filter_by(default=True).first()
```
接着要将这个插入角色的操作写进deploy命令，后面使用 flask deploy 即可部署
```
# run.py
@app.cli.command()
def deploy():
    Role.insert_roles()
```

# flask-migrate 
```
pipenv install flask-migrate
```
运行创建数据库表
```
flask db init 
flask db migrate -m "add users and roles table"
flask db upgrade 
```

# 单元测试
先配置flask 命令
```py
# run.py
@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```
新建 tasks 文件夹 在根文件夹下
```
mkdir tests
```
新建单元测试文件
```py
# tests/test_user_models.py
# 用户模型测试脚本
import unittest
from app.auth.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_enter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)
    
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password
    
    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
    
    def test_password_salts_are_random(self):
        u = User(password="cat")
        u1 = User(password = "cat")
        self.assertFalse(u1.password_hash == u.password_hash)

# 角色模型测试脚本
# tests/test_user_role.py
import unittest
from app.auth.models import Role,Permission,User

class TestUserRole(unittest.TestCase):
    def test_default_user(self):
        u = User(username="john",password="cat")
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.FOLLOW))
    
    def test_moderator_user(self):
        u = User(username="john_moder",password="123")
        u.role = Role.query.filter_by(name="Moderator").first()
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
    
    def test_admin_user(self):
        u = User(username="john_admin",password="123")
        u.role = Role.query.filter_by(name="ADMIN").first()
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.ADMIN))
```
## 运行部署初始化和单元测试
```
flask deploy
flask test 
```