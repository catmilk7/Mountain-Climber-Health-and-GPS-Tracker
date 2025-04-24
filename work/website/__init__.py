from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()  # Load the .env file

from os import path
import os

db = SQLAlchemy()
mail = Mail()

DB_NAME = "database.db"
DB_FOLDER = "website"
DB_PATH = os.path.join(os.getcwd(), DB_FOLDER, DB_NAME)  # Get absolute path

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcdefg'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'  # Ensure absolute path
    
        # Email config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    
    db.init_app(app)
    mail.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists(DB_FOLDER):  # Ensure folder exists
        os.makedirs(DB_FOLDER, exist_ok=True)  # Create directory safely
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database Created at:', DB_PATH)

