# coding: utf-8 
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from flask import current_app

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12))
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __init__(self,**kw):
        super(User,self).__init__(**kw)
        # 分配管理员角色
        if self.role is None and self.email == current_app.config['ADMIN']:
            self.role = Role.query.filter_by(name="ADMIN").first()

        # 如果一个用户的角色不存在
        if self.role is None:
            # 分配一个默认角色
            self.role = Role.query.filter_by(default=True).first()
    
    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm) 
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    @property
    def password(self):
        raise AttributeError("password is not readable attribute")
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))
    default = db.Column(db.Boolean,default=False,index=True)
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
    def reset_permission(self):
        self.permissions = 0    
    
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

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

# from flask_login import AnonymousUserMixin,UserMixin
# class Anonymous(AnonymousUserMixin):
#     def can(self,perm):
#         return False
    
#     def is_administrator(self,perm):
#         return False

