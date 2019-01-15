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

