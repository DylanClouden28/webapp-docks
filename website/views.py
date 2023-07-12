from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import login_required
from wtforms import StringField, RadioField, SubmitField
from . import db
from .models import Boat
import re

views = Blueprint('views', __name__)

class BoatLogForm(FlaskForm):
    boat_reg = StringField('Boat Registration')
    boat_name = StringField('Boat Name')
    boat_size = RadioField('Boat Size', choices=[('0-25','25 feet and Under'), ('26-40', '26 feet to 40'), ('41-Over', '41 feet and over')])
    owner_name = StringField('Owner\'s Name')
    phone_number = StringField('Phone Number')
    email = StringField('Email')
    zipcode = StringField('Zipcode or Postal Code')
    submit = SubmitField('Submit')


@views.route('/')
@login_required
def home():
    return render_template("home.html")

@views.route('/boatlog')
@login_required
def boatlog():
    return render_template("boatlog.html")

@views.route('/log-boat', methods=['GET', 'POST'])
@login_required
def log_boat():
    form = BoatLogForm()
    if form.validate_on_submit():
        if request.method == "POST":
            print(form.boat_size.data)
            boat_reg = form.boat_reg.data.lower().replace(" ", "")
            boat_name = form.boat_name.data.lower().replace(" ", "")
            owner_name = form.owner_name.data.lower()
            phone_number = re.sub("[^0-9]", "", form.phone_number.data)
            email = form.email.data.lower().replace(" ", "")
            zipcode = form.zipcode.data.lower().replace(" ", "")
            boat_size = form.boat_size.data
            if not boat_reg and not boat_name:
                flash('Boat Registration or Boat Name is required.', category="error")
                return render_template("log-boat.html", form=form)
            elif not phone_number.isdigit() and phone_number:
                flash('Phone Number must only contain numbers.', category="error")
                return render_template("log-boat.html", form=form)
            boat = None
            if boat_reg:
                boat = Boat.query.filter_by(boat_reg=boat_reg).first()
            elif boat_name:
                boat = Boat.query.filter_by(boat_name=boat_name).first()
            if boat:
                flash('Boat already exists', category="error")
            elif boat_reg or boat_name:
                new_boat = Boat(boat_reg=boat_reg, boat_name=boat_name, boat_size=boat_size, owner_name=owner_name, phone_number=phone_number, email=email, zipcode=zipcode)
                db.session.add(new_boat)
                db.session.commit()
                flash("Boat Logged!", category="success")
                return redirect(url_for('views.home'))
    else:
        print(form.errors)
    return render_template("log-boat.html", form=form)
