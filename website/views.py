from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import or_
from . import db
from .models import Boat, CurrentBoats
from .forms import BoatLogForm, SearchForm, PaymentForm
from .functions import addBoatToDB, searchBoatInDB, getBoatInDB, updateBoatInfo, getBoatById, add_payment
import re

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html")

@views.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if request.method == "POST":
            button_pressed = request.form.get('submit-button')
            print("Button pressed is: " + str(button_pressed))
            if button_pressed == 'search':
                return searchBoatInDB('search.html', form)
            if button_pressed == 'add':
                return redirect(url_for('views.log_boat', boat_reg=form.boat_reg.data, boat_name=form.boat_name.data, phone_number=form.phone_number.data))
    results = []
    resultsToday = []
    if CurrentBoats.query.first():
        resultsToday = CurrentBoats.query.first().boats.all()
        print(resultsToday)
    return render_template('search.html', form=form, boats=results, currentboats=resultsToday)



@views.route('/log-boat', methods=['GET', 'POST'])
@login_required
def log_boat():
    form = BoatLogForm()
    if form.validate_on_submit():
        if request.method == "POST":
            button_pressed = request.form.get('submit-button')
            print("Button pressed is: " + str(button_pressed))
            if button_pressed == 'log':
                return addBoatToDB('log-boat.html', form)
            elif button_pressed == 'update':
                currentboatID = request.args.get('id', '')
                result = getBoatById(currentboatID)
                updateBoatInfo(form, result)
                flash('Succesfully updated boater information', category='success')
                return redirect(url_for('views.search'))
            elif button_pressed == 'visits':
                currentboatID = request.args.get('id', '')
                return redirect(url_for('views.visits', id=currentboatID))
    else:
        print(form.errors)
    if request.method == "GET":
        form.boat_reg.data = boat_reg = request.args.get('boat_reg', '')
        form.boat_name.data = request.args.get('boat_name', '')
        form.phone_number.data = request.args.get('phone_number', '')
        result = getBoatInDB(form)
        print(result)
        if result:
           form.boat_reg.data = result.boat_reg
           form.boat_name.data = result.boat_name
           form.phone_number.data = result.phone_number
           form.boat_size.data = result.boat_size
           form.owner_name.data = result.owner_name
           form.email.data = result.email
           form.zipcode.data = result.zipcode
    return render_template("log-boat.html", form=form)

@views.route('/visits' , methods=['GET','POST'])
@login_required
def visits():
    form = PaymentForm()
    boat = getBoatById(request.args.get('id', ''))
    if form.validate_on_submit():
        if request.method == "POST":
            add_payment("visits.html", form, boat)

    if not boat:
        flash("Bad Boat ID", category='error')
    print("Visits: ", boat.visits)
    return render_template("visits.html", form=form, boat=boat)
