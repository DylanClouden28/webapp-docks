from . import db
from datetime import datetime, timezone
from flask import Flask, flash, render_template, redirect, url_for
from flask_login import current_user
from .models import Boat, CurrentBoats, Visit
from sqlalchemy import or_
import re

def printBoat(Boat):
    print('---------------------------------')
    print("ID: " + str(Boat.id))
    print("Boat Reg: " + Boat.boat_reg)
    print("Sanitized Boat Reg: " + Boat.sanitized_boat_reg)
    print("Boat Name: " + Boat.boat_name)
    print("Sanitized Boat Name: " + Boat.sanitized_boat_name)
    print("Phone Number: " + Boat.phone_number)
    print("Sanitized Phone Number: " + Boat.sanitized_phone_number)
    print("Owner Name: " + Boat.owner_name)
    print("Sanitized Owner Name: " + Boat.sanitized_owner_name)
    print("Email: " + Boat.email)
    print("Zipcode: " + Boat.zipcode)

def printBoats(Boats):
    for Boat in Boats:
        print('---------------------------------')
        print("ID: " + str(Boat.id))
        print("Boat Reg: " + Boat.boat_reg)
        print("Sanitized Boat Reg: " + Boat.sanitized_boat_reg)
        print("Boat Name: " + Boat.boat_name)
        print("Sanitized Boat Name: " + Boat.sanitized_boat_name)
        print("Phone Number: " + Boat.phone_number)
        print("Sanitized Phone Number: " + Boat.sanitized_phone_number)
        print("Owner Name: " + Boat.owner_name)
        print("Sanitized Owner Name: " + Boat.sanitized_owner_name)
        print("Boat Size: " + str(Boat.boat_size))


def sanitize(string):
    return re.sub(r'\W+', '', string).lower()

def no_whitespace_lowercase(string):
    return ''.join(string.split()).lower()

def getBoatById(id):
    boat = Boat.query.get(id)
    if boat is None:
        flash('No boat with given ID found', 'error')
        return None
    else:
        return boat

def updateBoatInfo(form, boat):
    if form.boat_reg.data:
        boat.boat_reg = form.boat_reg.data
        boat.sanitized_boat_reg = sanitize(form.boat_reg.data)
    if form.boat_name.data:
        boat.boat_name = form.boat_name.data
        boat.sanitized_boat_name = sanitize(form.boat_name.data)
    if form.phone_number.data:
        boat.phone_number = form.phone_number.data
        boat.sanitized_phone_number = sanitize(form.phone_number.data)

    if form.owner_name.data:
        boat.owner_name = form.owner_name.data
        boat.sanitized_owner_name = sanitize(form.owner_name.data)

    if form.boat_size.data:
        boat.boat_size = form.boat_size.data

    if form.phone_number.data:
        boat.email = form.email.data
    if form.zipcode.data:
        boat.zipcode = form.zipcode.data 
    db.session.commit()

def searchBoatInDB(current_page, form):
    sanitized_boat_reg = sanitize(form.boat_reg.data)
    sanitized_boat_name = sanitize(form.boat_name.data)
    sanitized_phone_number = sanitize(form.phone_number.data)
    conditions = []
    results = []
    resultsToday = []
    if sanitized_boat_reg:
        conditions.append(Boat.sanitized_boat_reg.contains(sanitized_boat_reg))
    if sanitized_boat_name:
        conditions.append(Boat.sanitized_boat_name.contains(sanitized_boat_name))
    if sanitized_phone_number:
        conditions.append(Boat.sanitized_phone_number.contains(sanitized_phone_number))
    if conditions:
        results = Boat.query.filter(or_(*conditions)).all()
        resultsToday = CurrentBoats.query.first().boats.filter(or_(*conditions)).all()
    else:
        resultsToday = CurrentBoats.query.first().boats.all()
        return render_template(current_page, form=form, boats=results, currentboats=resultsToday)
    
    if not resultsToday or not results:
        flash('No Boats Found in Database', category='error')  
    print(results)
    return render_template(current_page, form=form, boats=results, currentboats=resultsToday)

def BoatInCurrentBoats(form):
    sanitized_boat_reg = sanitize(form.boat_reg.data)
    sanitized_boat_name = sanitize(form.boat_name.data)
    sanitized_phone_number = sanitize(form.phone_number.data)
    conditions = []
    results = []
    resultsToday = []
    if sanitized_boat_reg:
        conditions.append(Boat.sanitized_boat_reg.contains(sanitized_boat_reg))
    if sanitized_boat_name:
        conditions.append(Boat.sanitized_boat_name.contains(sanitized_boat_name))
    if sanitized_phone_number:
        conditions.append(Boat.sanitized_phone_number.contains(sanitized_phone_number))
    if conditions:
        resultsToday = CurrentBoats.query.first().boats.filter(or_(*conditions)).all()
    if len(resultsToday) > 1:
        flash('Error more than version of this boat found in Database', category='error')
        print("ERROR MORE THAN 1 BOAT FOUND, RESULTS: ", resultsToday)
        return -1
    elif len(resultsToday) == 1:
        return resultsToday[0]
    else:
        return []
    
def getBoatInDB(form):
    sanitized_boat_reg = sanitize(form.boat_reg.data)
    sanitized_boat_name = sanitize(form.boat_name.data)
    sanitized_phone_number = sanitize(form.phone_number.data)
    conditions = []
    results = []
    resultsToday = []
    if sanitized_boat_reg:
        conditions.append(Boat.sanitized_boat_reg.contains(sanitized_boat_reg))
    if sanitized_boat_name:
        conditions.append(Boat.sanitized_boat_name.contains(sanitized_boat_name))
    if sanitized_phone_number:
        conditions.append(Boat.sanitized_phone_number.contains(sanitized_phone_number))
    if conditions:
        results = Boat.query.filter(*conditions).all()
    if len(results) > 1:
        flash('Error more than version of this boat found in Database', category='error')
        return -1
    elif len(results) == 1:
        return results[0]
    else:
        return []

def addBoatToDB(current_page, form):
    boat_reg = form.boat_reg.data
    boat_name = form.boat_name.data
    phone_number = form.phone_number.data
    owner_name = form.owner_name.data

    email = no_whitespace_lowercase(form.email.data)
    zipcode = sanitize(form.zipcode.data)
    boat_size = form.boat_size.data

    #Removes bad characters
    sanitized_boat_reg = sanitize(form.boat_reg.data)
    sanitized_boat_name = sanitize(form.boat_name.data)
    sanitized_phone_number = sanitize(form.phone_number.data)
    sanitized_owner_name = sanitize(form.owner_name.data)
    print(sanitized_boat_name)
    print(sanitized_boat_reg)

    if not sanitized_boat_reg and not sanitized_boat_name:
        flash('Boat Registration or Boat Name is required.', category="error")
        return render_template(current_page, form=form)
    elif not sanitized_phone_number and phone_number:
        flash('Phone Number must only contain numbers.', category="error")
        return render_template(current_page, form=form)
    boat = None
    if boat_reg:
        boat = Boat.query.filter_by(sanitized_boat_reg=sanitized_boat_reg).first()
    elif boat_name:
        boat = Boat.query.filter_by(sanitized_boat_name=sanitized_boat_name).first()

    
    if boat_reg or boat_name:
        #Not in Database
        if not boat:
            new_boat = Boat(boat_reg=boat_reg, boat_name=boat_name, boat_size=boat_size, owner_name=owner_name, phone_number=phone_number, email=email, zipcode=zipcode, sanitized_boat_name=sanitized_boat_name, sanitized_boat_reg=sanitized_boat_reg, sanitized_owner_name=sanitized_owner_name, sanitized_phone_number=sanitized_phone_number)
        #In database
        else:
            new_boat = boat

        current_boats = CurrentBoats.query.first()
        if not current_boats:
            current_boats = CurrentBoats()
            db.session.add(current_boats)

        #Adds boat to CurrentBoats with new Visit
        new_visit = None
        if not BoatInCurrentBoats(form):
            print("Creating New Visit")
            new_boat.current_boats_id = current_boats.id
            new_visit = Visit(
                logged_by = current_user.id,
                date_in = datetime.now(timezone.utc),
            )
            print(new_visit)
        printBoat(new_boat)
        print(current_boats.boats)
        if not boat:
            db.session.add(new_boat)
            db.session.commit()
            new_boat = Boat.query.filter_by(boat_reg=boat_reg, boat_name=boat_name).first()
        if new_visit:
            new_visit.boat_id = new_boat.id
            db.session.add(new_visit)
        db.session.commit()

        if new_visit:
            flash("New Visit Logged!", category="success")
        if not boat:
            flash("New Boat Added To DB!", category="success")
        if not new_visit and boat:
            flash("Boat Already Logged!", category="error")
        return redirect(url_for('views.search'))

def calcPrice(boat, days, nights, enw):
    size = boat.boat_size
    daysTotal = 0
    nightsTotal = 0
    enwTotal = 0
    if enw:
        enwTotal = 5
    if size == "0-25":
        if days > 0:
            daysTotal = 15 * days
        if nights > 0:
            nightsTotal = (25 + enwTotal) * nights
    elif size == "26-40":
        if days > 0:
            daysTotal = 20 * days
        if nights > 0:
            nightsTotal = (30 + enwTotal) * nights
    elif size == "41-Over":
        if days > 0:
            daysTotal = 25 * days
        if nights > 0:
            nightsTotal = (35 + enwTotal) * nights

    return daysTotal, nightsTotal

def edit_payment(visitid, form):
    sanitize_paid_days = sanitize(form.paid_days.data)
    sanitize_paid_nights = sanitize(form.paid_nights.data)
    paid_enw = form.paid_enw.data
    paid_with = form.paid_with.data
    current_visit = Visit.query.get(visitid)
    boat = getBoatById(current_visit.boat_id)
    current_visit.paid_days = sanitize_paid_days
    current_visit.paid_nights = sanitize_paid_nights
    if paid_enw == "Yes":
        current_visit.paid_enw = True
    else:
        current_visit.paid_enw = False
    current_visit.paid_with = paid_with
    daysTotal, nightsTotal = calcPrice(boat, int(sanitize_paid_days), int(sanitize_paid_nights), current_visit.paid_enw)
    current_visit.paid_amount = daysTotal + nightsTotal
    lastTotal = 0
    if len(boat.visits) > 1:
        lastTotal = boat.visits[-2].total
    current_visit.total = lastTotal + current_visit.paid_amount
    current_visit.date_paid = datetime.now(timezone.utc)
    db.session.commit()

def add_payment(current_page, form, boat):
    sanitize_paid_days = sanitize(form.paid_days.data)
    sanitize_paid_nights = sanitize(form.paid_nights.data)
    paid_enw = form.paid_enw.data
    paid_with = form.paid_with.data
    current_visit = None

    if boat.current_boats_id:
        current_visit = boat.visits[-1]

    current_visit.paid_days = sanitize_paid_days
    current_visit.paid_nights = sanitize_paid_nights
    if paid_enw == "Yes":
        current_visit.paid_enw = True
    else:
        current_visit.paid_enw = False
    current_visit.paid_with = paid_with
    daysTotal, nightsTotal = calcPrice(boat, int(sanitize_paid_days), int(sanitize_paid_nights), current_visit.paid_enw)
    current_visit.paid_amount = daysTotal + nightsTotal
    lastTotal = 0
    if len(boat.visits) > 1:
        lastTotal = boat.visits[-2].total
    current_visit.total = lastTotal + current_visit.paid_amount
    current_visit.date_paid = datetime.now(timezone.utc)
    db.session.commit()

        