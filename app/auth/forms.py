# coding: utf-8 
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Length,Email,EqualTo,Regexp
from .models import User


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Keep me Logged in")
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    email = StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    password1 = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password Confirm",validators=[DataRequired(),EqualTo('password1')])    
    submit = SubmitField("Register")

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email registered")
    
    def validate_name(self,filed):
        if User.query.filter_by(name=filed.data).first():
            raise ValidationError("name registered")


class ResetPasswdForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired()])
    password1 = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password Confirm",validators=[DataRequired(),EqualTo('password1')])    
    submit = SubmitField("Reset Password")


class ForgetPasswordForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Length(1,64),Email()])
    submit = SubmitField("Forget Password!")


class ResetForgetPasswordForm(FlaskForm):
    password1 = PasswordField("Password",validators=[DataRequired()])
    password2 = PasswordField("Password Confirm",validators=[DataRequired(),EqualTo('password1')])    
    submit = SubmitField("Reset Password")