import unittest
from flask import current_app
from app.utils.encrypt import encrypt_forget_passwd_token,verify_forget_passwd_token
from binascii import b2a_hex,a2b_hex
class TestForgetPasswdToken(unittest.TestCase):
    def test_verify_token(self):
        token = encrypt_forget_passwd_token("1234567890123456","john.wen@123.com")
        self.assertTrue(verify_forget_passwd_token('1234567890123456',token,3600))
        token2 = encrypt_forget_passwd_token("1234567890123456","john.wen111@123.com")
        self.assertFalse(verify_forget_passwd_token('1234567890123456',token2,3600))
        token3 = encrypt_forget_passwd_token("1234567890123456","john.wen@123.com")
        self.assertFalse(verify_forget_passwd_token("1234567890123456",token3,0))

        