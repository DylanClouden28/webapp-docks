from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import or_
from . import db
from .models import Boat, CurrentBoats, Visit, User
from .forms import BoatLogForm, SearchForm, PaymentForm, DeleteVisitForm
from .functions import addBoatToDB, searchBoatInDB, getBoatInDB, updateBoatInfo, getBoatById, add_payment, edit_payment, add_visit, sort_key, remove_visit, calcCurrentBoatStatus,calc_current_time
import re
from datetime import datetime, timezone

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html")

@views.route('/checkout')
def checkout():
    return render_template('checkout.html')

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
        for boat in resultsToday:
            calcCurrentBoatStatus(boat)
        #After checks are made and transients are removed
        resultsToday = CurrentBoats.query.first().boats.all()
    return render_template('search.html', form=form, boats=results, currentboats=resultsToday, current_time=calc_current_time())



@views.route('/log-boat', methods=['GET', 'POST'])
@login_required
def log_boat():
    form = BoatLogForm()
    sorted_visits = None
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
                boat = getBoatById(currentboatID)
                return redirect(url_for('views.visits', id=currentboatID, boat=boat))
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
           if result.visits:
               sorted_visits = sorted(result.visits, key=sort_key, reverse=True)
    return render_template("log-boat.html", form=form, boat=result, visits=sorted_visits)

@views.route('/visits' , methods=['GET','POST'])
@login_required
def visits():
    form = PaymentForm()
    delete_visit_form = DeleteVisitForm()
    button_pressed = request.form.get('submit-button')
    selected_row_id = request.form.get('selectedRowId')
    print("Button pressed is: " + str(button_pressed))
    print("Selected row ID is:", selected_row_id)
    
    boat = getBoatById(request.args.get('id', ''))
    sorted_visits = sorted(boat.visits, key=sort_key, reverse=True)
    if button_pressed == "search":
        form.date_paid.data = calc_current_time()
        form.date_in.data = Visit.query.get(selected_row_id).date_in

    if not boat:
        flash("Bad Boat ID", category='error')
    if request.method == "POST":
        if button_pressed == "delete":
            if delete_visit_form.validate_on_submit():
                remove_visit_id = delete_visit_form.selecteddeleteRowId.data
                print("Remove visit ID:", remove_visit_id)
                remove_visit(remove_visit_id)
            else:
                flash("form invalid" + str(form.errors), category="error")
        else:
            if form.validate_on_submit():
                    if button_pressed == "search":
                        add_payment("visits.html", form, boat, id=selected_row_id)
            elif button_pressed == "add_new":
                form.paid_days.data = "0"
                form.paid_nights.data = "0"
                form.paid_enw.data = None
                print("add new visit")
                add_visit("visits.html", form, boat)
            else:
                flash("form invalid" + str(form.errors), category="error")
    boat = getBoatById(request.args.get('id', ''))
    sorted_visits = sorted(boat.visits, key=sort_key, reverse=True)
    return render_template("visits.html", form=form, boat=boat, visits=sorted_visits, delete_form=delete_visit_form)

@views.route('/update_payment', methods=['POST'])
def update_payment():
    form = PaymentForm(request.form)
    boat = getBoatById(request.args.get('id', ''))
    visitid = request.args.get('visitid', '')
    if form.validate():
        edit_payment(visitid, form)
        return redirect(url_for('views.visits', id=boat.id))
    else:
        print(form.errors)
        flash("Invalid form reload or relogin" + str(form.errors), category="error")
        return redirect(url_for('views.visits', id=boat.id))
    
@views.route('/phone', methods=['POST', 'GET'])
def phone():
    phone_number_Form = PhoneNumber()
    if phone_number_Form.validate_on_submit():
        num = phone_number_Form.phone_number.data
        boat = get_boat_phone_number(num)
        print(num)
        if boat is None:
            return redirect(url_for('views.public', phone_number=num))
        return redirect(url_for('views.pay', phone_number=num))
    return render_template("phone.html", form=phone_number_Form)

@views.route('/public_login', methods=['POST', 'GET'])
def public():
    login_form = BoatLogForm
    if login_form.validate_on_submit():
        addBoatToDB(PublicLogin)
    phone_number = request.args.get('phone_number')

    return render_template("payment.html")

@views.route('/pay', methods=['POST', 'GET'])
def pay():
    phone_number = request.args.get('phone_number')
    boat = get_boat_phone_number(phone_number)
    boat_registration = boat.boat_reg
    boat_size = boat.boat_size
    owner = boat.owner_name
    return render_template('payment.html', phone_number=phone_number, owner=owner, boat_size=boat_size, boat_registration=boat_registration)