from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from website.config import SECRET_KEY
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import pytz

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    csrf = CSRFProtect(app)
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User

    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.template_filter('utc_to_est')
    def utc_to_est_filter(s):
        if s == None:
            return "None"
        fmt = "%Y-%m-%d %H:%M:%S.%f+00:00"
        utc_datetime = datetime.strptime(s, fmt)

        est_tz = pytz.timezone('US/Eastern')
        est_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(est_tz)

        return est_datetime.strftime('%Y-%m-%d %I:%M %p')
    
    @app.template_filter('userID_to_name')
    def userID_to_name(s):
        user = load_user(int(s))
        return user.first_name


    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')