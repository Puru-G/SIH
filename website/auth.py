from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Application
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from website import Mail_function
from datetime import datetime
import uuid

app=Mail_function()
auth = Blueprint('auth', __name__)

@auth.route('/signup',methods=['GET','POST'])
def signup():
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
        elif(len(str(phone))!=10):
            flash('Enter valid phone number!!',category='error')
        elif(len(password)<8):
            flash('Length of password must be between 8 and 15!!',category='error')
        elif(confirm_password!=password):
            flash('Password Does not match!!',category='error')
        else:
            new_user=User(email=email,first_name=first_name,middle_name=middle_name,last_name=last_name,phone=phone,password=generate_password_hash(password , method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account Created!!',category='Success')
            return redirect(url_for('views.home'))
        
    return render_template('signup.html',user=current_user)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login',methods=['GET','POST'])
def login():
    if(request.method=="POST"):

        email=request.form.get('email')
        password=request.form.get('password')   
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):

                flash('Logged in successfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password,try again.', category='error')
        else:
            flash('Email does not exist.', category='error')




    return render_template("login.html",user=current_user)



@auth.route('/contact',methods=['GET','POST'])
def contact():
    if(request.method == "POST"):
        name =  request.form.get('name')
        gender =  request.form.get('gender')
        dob =  datetime.strptime(request.form.get('dob'),'%Y-%M-%d').date()
        email=  request.form.get('email')
        phone =  str(request.form.get('phone'))
        college_mail =  request.form.get('College')
        eno = request.form.get('eno')
        sem = request.form.get('semester')
        city =  request.form.get('city')
        state =  request.form.get('state')
        # domicile_certificate = request.files['domicile']
        # domicile_filename = domicile_certificate.filename
        aadhar = request.form.get('aadhar')
        def check(var):
            return any(char.isdigit() for char in var)
        
        if(check(name) or check(state) or check(city)):
            flash('Name contains number!!',category='error')
        elif(len(email)<=10 or len(college_mail)<=10):
            flash('Email is not valid!!',category='error') 
        elif(len(phone)!=10):
            flash('Enter valid phone number!!',category='error')
        elif(len(aadhar)!=12):
            flash("Enter valid Aadhar Number!!!")
        else:
            unique_code = str(uuid.uuid3(uuid.NAMESPACE_URL,aadhar))

            new_application = Application(name=name,gender=gender,dob=dob,email=email,phone=phone,college_mail=college_mail,eno=eno,sem=sem,city=city,state=state,aadhar=aadhar,unique_code=unique_code)#domicile_certificate=domicile_certificate.read()
            db.session.add(new_application)
            db.session.commit()
        


            mail=Mail(app)
            msg=Message(subject="CONGRATULATIONS It WORKS!!!!!!",sender='phoenix.12456789@gmail.com',recipients=['rohan111bhargava@gmail.com'])
            application_body = "Name : "+name+"\n"+"Gender : "+gender+"\n"+"DOB : "+str(dob)+"\n"+"Gmail : "+email+"\n"+"Phone : "+phone+"\n"+"College : "+college_mail+"\n"+"EnormentNo: "+eno+"\n"+"Semester: "+sem+"\n"+"State : "+state+"\n"+"City : "+city+"\n"+"Aadhar Card Number : "+aadhar
            msg.body = application_body + "\n\n"+"Once verification is completed send below code to Student."+"\n\n"+"Code : "+unique_code

            # msg.attach("File",domicile_filename+"/pdf","pdf")
            mail.send(msg)
            return render_template('under_process.html')
        

    return render_template('contact.html')

@auth.route('/search',methods=['GET','POST'])
def search():
     if(request.method=="POST"):
        if(request.form.get('col')=="others"):
            if(len(request.form.get("college_name"))!=0 and len(request.form.get("code"))!=0):
                unique_code = request.form.get('code')
                check_code = Application.query.filter_by(unique_code=unique_code).first()
                if check_code:
                    flash('Congratulation!!!  Now you can procced to fill the scholarship details!!',category='success')
                    return render_template('scholarship.html')
                else:
                    flash('Enter Valid Code',category='error') 
            else:
                return render_template('contact.html')
        else:
            return render_template('scholarship.html')
     
     
     return render_template('searchinstitute.html')

