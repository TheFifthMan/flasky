# coding: utf-8 
from flask import Blueprint
auth_bp = Blueprint("/",__name__)

from . import views,routes,models
