from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import or_
from . import db
from .models import Boat, CurrentBoats
from .forms import BoatLogForm, SearchForm
from .functions import addBoatToDB, searchBoatInDB, searchDBforexistingdata
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
            return searchBoatInDB('search.html', form)
    results = []
    resultsToday = CurrentBoats.query.first().boats.all()
    print(results)
    print(resultsToday)
    return render_template('search.html', form=form, boats=results, currentboats=resultsToday)



@views.route('/log-boat', methods=['GET', 'POST'])
@login_required
def log_boat():
    form = BoatLogForm()
    if form.validate_on_submit():
        if request.method == "POST":
            return addBoatToDB('log-boat.html', form)
    else:
        print(form.errors)
    if request.method == "GET":
        form.boat_reg.data = boat_reg = request.args.get('boat_reg', '')
        form.boat_name.data = request.args.get('boat_name', '')
        form.phone_number.data = request.args.get('phone_number', '')
        result = searchDBforexistingdata(form)
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
