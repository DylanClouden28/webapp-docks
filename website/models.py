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
    def serialize(self):
        return {
            'id': self.id, 
            'boat_reg': self.boat_reg,
            'boat_name': self.boat_name,
            'boat_size': self.boat_size,
            'owner_name': self.owner_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'zipcode': self.zipcode,
            'visits': [visit.serialize for visit in self.visits]
        }

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
    def serialize(self):
        return {
            'id': self.id, 
            'logged_by': self.logged_by,
            'date_in': self.date_in,
            'date_paid': self.date_paid,
            'paid_amount': self.paid_amount,
            'paid_days': self.paid_days,
            'paid_nights': self.paid_nights,
            'paid_enw': self.paid_enw,
            'paid_with': self.paid_with,
            'unpaid_days': self.unpaid_days,
            'unpaid_nights': self.unpaid_nights,
            'boat_id': self.boat_id
        }
