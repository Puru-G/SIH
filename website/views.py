from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db 
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message

views = Blueprint('views', __name__)


@views.route('/',methods=['GET','POST'])
@login_required
def home():
    return render_template("home.html")