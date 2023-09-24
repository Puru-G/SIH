from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail, Message
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)


    from .views import views
    from .auth import auth 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    with app.app_context():
        db.create_all()

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def laod_user(id):
        return User.query.get(int(id))

    return app

def Mail_function():
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']='phoenix.12456789@gmail.com'
    app.config['MAIL_PASSWORD']='ppim ojed dvma joue'
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True 

    return app