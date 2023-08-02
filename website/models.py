from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
import re

def sanitize(input_string):
    return re.sub(r'\W+', '', input_string).lower()

class CurrentBoats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boats = db.relationship('Boat', lazy='dynamic')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    logs = db.relationship('Visit')

class Boat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Caching aplhanumeric forms for search
    boat_reg = db.Column(db.String(150), unique=True)
    sanitized_boat_reg = db.Column(db.String(150), unique=True)

    boat_name = db.Column(db.String(150))
    sanitized_boat_name = db.Column(db.String(150))

    phone_number = db.Column(db.String(150))
    sanitized_phone_number = db.Column(db.String(150))

    owner_name = db.Column(db.String(150))
    sanitized_owner_name = db.Column(db.String(150))

    boat_size = db.Column(db.Integer)


    email = db.Column(db.String(150))
    zipcode = db.Column(db.String(150))
    visits = db.relationship('Visit', backref='boat')
    current_boats_id = db.Column(db.Integer, db.ForeignKey('current_boats.id'))

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logged_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_in = db.Column(db.String(150))
    date_paid = db.Column(db.String(150))
    paid_amount = db.Column(db.Float)
    paid_days = db.Column(db.Integer)
    paid_nights = db.Column(db.Integer)
    paid_enw = db.Column(db.Boolean)
    paid_with = db.Column(db.String(150))
    unpaid_days = db.Column(db.Integer)
    unpaid_nights = db.Column(db.Integer)
    boat_id = db.Column(db.Integer, db.ForeignKey('boat.id'))

class DebtBoats(db.Model):
    id = db.Column(db.Integer, primary_key=True)

