from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from website.config import SECRET_KEY
from flask_wtf.csrf import CSRFProtect
from flask_admin.contrib import sqla
from flask_admin.base import MenuLink
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
    from .payments import payments
    from .checkout import checkout
    from .good_payment import good_payment

    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_blueprint(payments)
    app.register_blueprint(checkout)
    app.register_blueprint(good_payment)
    csrf.exempt(payments)
    csrf.exempt(checkout)
    from .models import User, Boat, CurrentBoats, Visit, DebtBoats

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
    
    @app.template_filter('utc_to_est_short')
    def utc_to_est_filter(s):
        if s == None:
            return "None"
        fmt = "%Y-%m-%d %H:%M:%S.%f+00:00"
        utc_datetime = datetime.strptime(s, fmt)
        
        est_tz = pytz.timezone('US/Eastern')
        est_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(est_tz)
        
        month = est_datetime.month
        day = est_datetime.day
        year = est_datetime.year % 100  # Using the last two digits of the year
        
        hour = est_datetime.strftime('%I').lstrip('0')  # Remove leading zero
        minute = est_datetime.strftime('%M')
        time_period = est_datetime.strftime('%p')
        
        return f"{month}/{day}   {hour}:{minute}{time_period}"
    
    @app.template_filter('userID_to_name')
    def userID_to_name(s):
        user = load_user(int(s))
        return user.first_name

    @app.template_filter('reverse')
    def reverse_filter(sequence):
        return reversed(sequence)
    
    @app.template_filter('datetime_to_str')
    def datetime_to_str(datetime):
        return datetime.strftime('%Y-%m-%d %H:%M:%S.%f+00:00')
    
    @app.template_filter('has_paid')
    def has_paid(boat):
        from .functions import calc_current_time
        current_time = calc_current_time()
        return boat.paid_until and datetime_to_str(current_time) < boat.paid_until
    
    @app.errorhandler(400)
    def handle_400(error):
        return 'Bad Request: ' + str(error), 400

    
    class MyModel(sqla.ModelView):
      column_display_pk = True
      column_hide_backrefs = False

    class CurrentBoatView(MyModel):
        column_list = ('id', 'Current_Boats_list')
        def _list_boats(self, context, model, name):
            return ", ".join(str(boat.id) for boat in model.boats.all())
        column_formatters = {
            'Current_Boats_list': _list_boats
        }
    
    admin = Admin(app, 
                  name='NT Gateway Harbor', 
                  template_mode='bootstrap4'
                )
    admin.add_view(MyModel(User, db.session))
    admin.add_view(MyModel(Boat, db.session))
    admin.add_view(CurrentBoatView(CurrentBoats, db.session))
    admin.add_view(MyModel(Visit, db.session))
    admin.add_view(MyModel(DebtBoats, db.session))
    admin.add_link(MenuLink(name='Home', url='/', category='Links'))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')