from . import db
from .models import Boat, CurrentBoats, Visit
from datetime import datetime, timezone, timedelta
from .functions import calc_current_time, str_to_datetime, getBoatById, sanitize, no_whitespace_lowercase, printBoat, calcPaidUntil, calcPrice, sort_key
from flask import flash, render_template, redirect, url_for
from flask_login import current_user
from sqlalchemy import or_
import re

def boater_adds_payment(paid_items, boat_id):
    current_visit = None
    electric = None

    boat = getBoatById(boat_id)
    sorted_visits = sorted(boat.visits, key=sort_key, reverse=True)
    current_visit = sorted_visits[0]
    if boat:
        for item in paid_items:
            if "Day" in item["description"]:
                current_visit.paid_days = 1
            elif "Night" in item["description"]:
                current_visit.paid_nights = int(item["quantity"])
            
            if 'E&W' in item["description"]:
                electric = True
    current_visit.paid_enw = electric
    current_visit.paid_with = 'Charge'
    current_visit.date_paid = calc_current_time()
    calcPrice(boat)
    if current_visit.logged_by == None:
        current_visit.logged_by = 'Boater'
    if current_visit.payment_by == None:
        current_visit.payment_by = 'Boater'
    db.session.commit()

def updateBoatInfo(form, boat):
    if not boat.boat_reg:
        boat.boat_reg = form.boat_reg.data
        boat.sanitized_boat_reg = sanitize(form.boat_reg.data)
    if not boat.boat_name:
        boat.boat_name = form.boat_name.data
        boat.sanitized_boat_name = sanitize(form.boat_name.data)
    if not boat.phone_number:
        boat.phone_number = form.phone_number.data
        boat.sanitized_phone_number = sanitize(form.phone_number.data)

    if not boat.owner_name:
        boat.owner_name = form.owner_name.data
        boat.sanitized_owner_name = sanitize(form.owner_name.data)

    if not boat.boat_size:
        boat.boat_size = form.boat_size.data

    if not boat.zipcode:
        boat.zipcode = form.zipcode.data 
    db.session.commit()

def add_payment_to_Boat(boat_id, paid_items):
    boat = getBoatById(boat_id)
    sorted_visits = sorted(boat.visits, key=sort_key, reverse=True)
    current_visit = sorted_visits[0]
    if boat:
        for item in paid_items:
            if "Day" in item.description:
                current_visit.paid_days += 1
            elif "Night" in item.description:
                current_visit.paid_nights += 1

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
    
def addBoatToDB(current_page, form):
    boat_reg = form.boat_reg.data
    boat_name = form.boat_name.data
    phone_number = form.phone_number.data
    owner_name = form.owner_name.data
    zipcode = sanitize(form.zipcode.data)
    boat_size = form.boat_size.data

    nights = sanitize(form.total_nights.data)
    days = sanitize(form.day_fee.data)
    water_electric = sanitize(form.water_electric.data)

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
        flash('Phone Number must contain numbers.', category="error")
        return render_template(current_page, form=form)
    boat = None
    if boat_reg:
        boat = Boat.query.filter_by(sanitized_boat_reg=sanitized_boat_reg).first()
    elif boat_name:
        boat = Boat.query.filter_by(sanitized_boat_name=sanitized_boat_name).first()

    
    if boat_reg or boat_name:
        #Not in Database
        if not boat:
            new_boat = Boat(boat_reg=boat_reg, boat_name=boat_name, boat_size=boat_size, owner_name=owner_name, phone_number=phone_number, email='', zipcode=zipcode, sanitized_boat_name=sanitized_boat_name, sanitized_boat_reg=sanitized_boat_reg, sanitized_owner_name=sanitized_owner_name, sanitized_phone_number=sanitized_phone_number)
        #In database
        else:
            new_boat = boat
            updateBoatInfo(form, boat)


        current_boats = CurrentBoats.query.first()
        if not current_boats:
            current_boats = CurrentBoats()
            db.session.add(current_boats)

        #Adds boat to CurrentBoats with new Visit
        new_visit = None
        print("Owes a fee: ", (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())) and (new_boat.paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date())))
        print("Boat IN Current Boats: ", BoatInCurrentBoats(form))
        if not BoatInCurrentBoats(form) and not ( (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())) and (new_boat.paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date()))  ):
            print("Creating New Visit")
            new_boat.current_boats_id = current_boats.id
            new_visit = Visit(
                logged_by = 'BOATER',
                date_in = calc_current_time(),
                paid_days = 0,
                paid_nights = 0,
                unpaid_days = 0,
                unpaid_nights = 0,
            )
            print(new_visit)
        elif (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())) or (new_boat.paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date())):
            new_boat.current_boats_id = current_boats.id
            sorted_visits = sorted(new_boat.visits, key=sort_key, reverse=True)
            if sorted_visits:
                current_visit = sorted_visits[0]
                current_time = calc_current_time()
                if(current_visit.paid_days is not None and current_visit.paid_days > 0) or (current_visit.paid_nights is not None and current_visit.paid_nights > 0):
                    calcPaidUntil(new_boat)
                date_format = "%Y-%m-%d %H:%M:%S.%f%z"
                latest_date_in = datetime.strptime(new_boat.latest_date_in, date_format) if new_boat.latest_date_in else None
                paid_until = datetime.strptime(new_boat.paid_until, date_format) if new_boat.paid_until else None

                #if not new_boat.paid_until and (current_time - latest_date_in) > timedelta(hours=2) and (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())):
                #   current_visit.unpaid_days = 1
                #elif new_boat.paid_until and current_time > paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date()):
                #    current_visit.unpaid_days = 1
                calcPrice(new_boat)
            db.session.commit()

            
        printBoat(new_boat)
        if not boat:
            db.session.add(new_boat)
            db.session.commit()
            new_boat = Boat.query.filter_by(boat_reg=boat_reg, boat_name=boat_name).first()
        if new_visit:
            new_visit.boat_id = new_boat.id
            db.session.add(new_visit)
            new_boat.latest_date_in = new_visit.date_in
            new_boat.paid_until = None
            print("Added new Visit, lastest date in: ", new_boat.latest_date_in)
        db.session.commit()

        return redirect(url_for('checkout.create_checkout_session', days=days,nights=nights,electric=water_electric,size=boat_size,id=new_boat.id),code=307)