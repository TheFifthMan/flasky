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
        
                
        
        