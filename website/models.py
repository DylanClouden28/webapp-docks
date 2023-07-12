from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    logs = db.relationship('Visit')

class Boat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    boat_reg = db.Column(db.String(150), unique=True)
    boat_name = db.Column(db.String(150))
    boat_size = db.Column(db.Integer)
    owner_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(150))
    email = db.Column(db.String(150))
    zipcode = db.Column(db.String(150))
    visits = db.relationship('Visit')

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

