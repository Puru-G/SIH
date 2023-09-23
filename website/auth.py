from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Application
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from website import Mail_function
import os
from datetime import datetime

app=Mail_function()
auth = Blueprint('auth', __name__)


@auth.route('/logout',methods=['GET','POST'])
def logout():
    return redirect(url_for('views.home'))

@auth.route('/login',methods=['GET','POST'])
def login():
    if(request.method=="POST"):

        email=request.form.get('email')
        password=request.form.get('password')   
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):

                flash('Logged in successfully!',category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again.', category='error')
        else:
            flash('Email does not exist.', category='error')




    return render_template("login.html")



@auth.route('/contact',methods=['GET','POST'])
def contact():
    if(request.method == "POST"):
        name =  request.form.get('name')
        gender =  request.form.get('gender')
        dob =  datetime.strptime(request.form.get('dob'),'%Y-%M-%d').date()
        email=  request.form.get('email')
        phone =  request.form.get('phone')
        college =  request.form.get('College')
        sem = request.form.get('semester')
        city =  request.form.get('city')
        state =  request.form.get('state')
        domicile_certificate = request.files['domicile']
        domicile_filename = domicile_certificate.filename

        new_application = Application(name=name,gender=gender,dob=dob,email=email,phone=phone,college=college,sem=sem,city=city,state=state,domicile_certificate=domicile_certificate.read())
        db.session.add(new_application)
        db.session.commit()

        

        mail=Mail(app)
        msg=Message(subject="CONGRATULATIONS It WORKS!!!!!!",sender='phoenix.12456789@gmail.com',recipients=['rohan111bhargava@gmail.com'])
        msg.body ="Name : "+name+"\n"+"Gender : "+gender+"\n"+"DOB : "+str(dob)+"\n"+"Gmail : "+email+"\n"+"Phone : "+phone+"\n"+"College : "+college+"\n"+"State : "+state+"\n"+"City : "+city
        
        msg.attach("File",domicile_filename+"/pdf","pdf")
        mail.send(msg)

        return "added to database"
    return render_template('contact.html')

@auth.route('/search',methods=['GET','POST'])
def search():
     if(request.method=="POST"):
        return render_template('contact.html')
     
     
     return render_template('searchinstitute.html')

