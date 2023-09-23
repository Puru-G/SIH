from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db 
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message

views = Blueprint('views', __name__)


@views.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':

        first_name=request.form.get('fname')
        last_name=request.form.get('lname')
        middle_name=request.form.get('mname')
        email=request.form.get('email')
        phone=request.form.get('phone')
        password=request.form.get('password')
        confirm_password=request.form.get('confirm_password')

        def check(var):
            return any(char.isdigit() for char in var)
        

        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exists!!',category='error')
        elif(check(first_name) or check(last_name) or check(middle_name)):
            flash('Name contains number!!',category='error')
        elif(len(email)<=10):
            flash('Email is not valid!!',category='error')
        elif(len(phone)!=10):
            flash('Enter valid phone number!!',category='error')
        elif(len(password)<8):
            flash('Length of password must be between 8 and 15!!',category='error')
        elif(confirm_password!=password):
            flash('Password Does not match!!',category='error')
        else:
            new_user=User(email=email,first_name=first_name,middle_name=middle_name,last_name=last_name,phone=phone,password=generate_password_hash(password , method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!!',category='Success')
            return redirect(url_for('views.home'))

    return render_template("home.html")
