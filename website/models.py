from . import db
from flask_login import UserMixin
from flask_mail import Mail, Message
from sqlalchemy.sql import func


class Application(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    gender = db.Column(db.String(10)) 
    dob = db.Column(db.Date())
    email = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    college_mail = db.Column(db.String(150))
    eno = db.Column(db.String(15))
    sem  = db.Column(db.String(15))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    domicile_certificate = db.Column(db.LargeBinary)


class User(db.Model, UserMixin):
    id=db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(150),unique=True)
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(150))
    #relationship with another table to be write here  db.relationship('Application')

