from . import db
from datetime import datetime, timezone, timedelta
from flask import Flask, flash, render_template, redirect, url_for
from flask_login import current_user
from .models import Boat, CurrentBoats, Visit, User
from sqlalchemy import or_
import re
import pytz

def convert_est_to_utc(est_time_str: str) -> str:
    try:
        # Parse the string into a datetime object
        est_dt_naive = datetime.strptime(est_time_str, '%Y-%m-%d %I:%M %p')
        
        # Attach the EST timezone info
        eastern = pytz.timezone('US/Eastern')
        est_dt_aware = eastern.localize(est_dt_naive)

        # Convert to UTCd
        utc_dt = est_dt_aware.astimezone(pytz.utc)
        
        # Format datetime to string before returning
        return utc_dt.strftime('%Y-%m-%d %H:%M:%S.%f+00:00')

    except ValueError as e:
        raise ValueError("Bad format") from e

def sort_key(visit):
    if visit.date_in is None:
        return datetime.min
    return datetime.strptime(visit.date_in, '%Y-%m-%d %H:%M:%S.%f+00:00')

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
        if CurrentBoats.query.first():
            resultsToday = CurrentBoats.query.first().boats.filter(or_(*conditions)).all()
    else:
        if CurrentBoats.query.first():
            resultsToday = CurrentBoats.query.first().boats.all()
        return render_template(current_page, form=form, boats=results, currentboats=resultsToday)
    
    if not resultsToday and not results:
        flash('No Boats Found in Database', category='error')  
    print(results)
    return render_template(current_page, form=form, boats=results, currentboats=resultsToday, )

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
def str_to_datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f+00:00')
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
        print("Owes a fee: ", (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())) and (new_boat.paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date())))
        if not BoatInCurrentBoats(form) and not ( (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())) and (new_boat.paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date()))  ):
            print("Creating New Visit")
            new_boat.current_boats_id = current_boats.id
            new_visit = Visit(
                logged_by = current_user.id,
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
            current_visit = sorted_visits[0]
            current_time = calc_current_time()
            if(current_visit.paid_days is not None and current_visit.paid_days > 0) or (current_visit.paid_nights is not None and current_visit.paid_nights > 0):
                calcPaidUntil(new_boat)
            date_format = "%Y-%m-%d %H:%M:%S.%f%z"
            latest_date_in = datetime.strptime(new_boat.latest_date_in, date_format) if new_boat.latest_date_in else None
            paid_until = datetime.strptime(new_boat.paid_until, date_format) if new_boat.paid_until else None

            #if not new_boat.paid_until and (current_time - latest_date_in) > timedelta(hours=2) and (new_boat.latest_date_in and (calc_current_time().date() == str_to_datetime(new_boat.latest_date_in).date())):
            #    current_visit.unpaid_days = 1
            #elif new_boat.paid_until and current_time > paid_until and (calc_current_time().date() == str_to_datetime(new_boat.paid_until).date()):
             #   current_visit.unpaid_days = 1
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

        if new_visit:
            flash("New Visit Logged!", category="success")
        if not boat:
            flash("New Boat Added To DB!", category="success")
        if not new_visit and boat:
            flash("Boat Already Logged!", category="error")
        return redirect(url_for('views.search'))
def calc_current_time():
    Debug = False
    current_time = datetime.now(timezone.utc)

    days_offset = 0
    hours_offset = 10
    mins_offset = 0

    if Debug:
        current_time += timedelta(days=days_offset, hours=hours_offset, minutes=mins_offset)
    print("Current Time is: ", current_time, "| Debug is: ", Debug)
    return current_time


def calcCurrentBoatStatus(boat):
    current_time = calc_current_time()
    date_format = "%Y-%m-%d %H:%M:%S.%f%z"
    latest_date_in = datetime.strptime(boat.latest_date_in, date_format) if boat.latest_date_in else None
    paid_until = datetime.strptime(boat.paid_until, date_format) if boat.paid_until else None
    if (boat.total_unpaid_days is not None and boat.total_unpaid_days > 0) or (boat.total_unpaid_nights is not None and boat.total_unpaid_nights > 0):
        return
    
    #If boat is Transient and has not paid remove
    print("Boat latest time: ", boat.latest_date_in)

    current_boats = CurrentBoats.query.first()
    if not current_boats:
        current_boats = CurrentBoats()
        db.session.add(current_boats)
            
    if not boat.paid_until and (current_time - latest_date_in) > timedelta(hours=2):
        remove_from_current_Visits(boat.id)
        print("Removed Boat from Current Visits: ", boat.id)
    #If boat is past it's paid time remove 
    elif boat.paid_until and current_time > paid_until:
        remove_from_current_Visits(boat.id)
        print("Removed Boat from Current Visits: ", boat.id)


def calcPaidUntil(boat):
    sorted_visits = sorted(boat.visits, key=sort_key, reverse=True)
    days = sorted_visits[0].paid_days
    nights = sorted_visits[0].paid_nights if sorted_visits[0].paid_nights is not None else 0
    date_paid = sorted_visits[0].date_paid
    if date_paid is None:
        return
    print("Date Paid: ", date_paid)
    print("Sorted Visit [0] id: ", sorted_visits[0].id)
    if isinstance(date_paid, str):
        date_paid_without_offset = datetime.strptime(sorted_visits[0].date_paid[:-6], "%Y-%m-%d %H:%M:%S.%f")
        utc_offset = pytz.timezone('UTC').utcoffset(date_paid_without_offset)
        date_paid = date_paid_without_offset.replace(tzinfo=pytz.UTC) + utc_offset
    paid_until = date_paid + timedelta(days=int(nights))

    utc_timezone = pytz.timezone('UTC')

    est_tz = pytz.timezone('US/Eastern')
    est_time = paid_until.astimezone(est_tz)

    if int(days) > 0:
        hour = 23
        min = 59
    else:
        hour = 11
        min = 0
    new_est_time = est_time.replace(hour=hour, minute=min)

    paid_until_utc_time = new_est_time.astimezone(utc_timezone)
    boat.paid_until = paid_until_utc_time.strftime('%Y-%m-%d %H:%M:%S.%f+00:00')
    print(boat.paid_until)


def calcPrice(boat):
    size = boat.boat_size
    daysTotal = 0
    nightsTotal = 0
    enwTotal = 0
    boat.total_paid_days = 0
    boat.total_paid_nights = 0
    boat.total_unpaid_days = 0
    boat.total_unpaid_nights = 0
    sorted_visits = sorted(boat.visits, key=sort_key)

    for index, visit in enumerate(sorted_visits):
        daysTotal = 0
        nightsTotal = 0
        enwTotal = 0
        days = int(visit.paid_days) if visit.paid_days is not None else 0
        nights = int(visit.paid_nights) if visit.paid_nights is not None else 0
        if visit.paid_enw:
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
        visit.paid_amount = daysTotal + nightsTotal
        boat.total_paid_days += days
        boat.total_paid_nights += nights

        if index > 0:
            visit.total = sorted_visits[index - 1].total + visit.paid_amount
        else:
            visit.total = visit.paid_amount

    for index, visit in enumerate(sorted_visits):
        daysTotal = 0
        nightsTotal = 0
        enwTotal = 0
        days = int(visit.unpaid_days) if visit.unpaid_days is not None else 0
        nights = int(visit.unpaid_nights) if visit.unpaid_nights is not None else 0
        if visit.paid_enw:
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
        unpaid_total = -(daysTotal + nightsTotal)
        boat.total_unpaid_days += days
        boat.total_unpaid_nights += nights
        if index > 0:
            visit.unpaid_total = sorted_visits[index - 1].unpaid_total + unpaid_total
        else:
            visit.unpaid_total = unpaid_total
    calcPaidUntil(boat)
def edit_payment(visitid, form):
    sanitize_paid_days = sanitize(form.paid_days.data)
    sanitize_paid_nights = sanitize(form.paid_nights.data)

    sanitize_unpaid_days = sanitize(form.unpaid_days.data)
    sanitize_unpaid_nights = sanitize(form.unpaid_nights.data)
    paid_enw = form.paid_enw.data
    paid_with = form.paid_with.data
    current_visit = Visit.query.get(visitid)
    boat = getBoatById(current_visit.boat_id)
    current_visit.paid_days = sanitize_paid_days
    current_visit.paid_nights = sanitize_paid_nights
    current_visit.unpaid_days = sanitize_unpaid_days
    current_visit.unpaid_nights = sanitize_unpaid_nights
    if paid_enw == "Yes":
        current_visit.paid_enw = True
    else:
        current_visit.paid_enw = False
    current_visit.paid_with = paid_with
    

    if not form.date_in.data == current_visit.date_in:
        try:
            utc_result = convert_est_to_utc(form.date_in.data)
            current_visit.date_in = utc_result
        except ValueError:
            flash("Bad format for date", category="error")
    
    if current_visit.date_paid == None:
        current_visit.date_paid = calc_current_time()
    elif not form.date_paid.data == current_visit.date_paid:
        try:
            print("Current time utc value: ", current_visit.date_paid)
            utc_result = convert_est_to_utc(form.date_paid.data)
            current_visit.date_paid = utc_result
            print("New time utc value: ", current_visit.date_paid)
        except ValueError:
            flash("Bad format for date", category="error")

    if current_visit.logged_by == None:
        user = User.query.get(int(current_user.id))
        current_visit.logged_by = user.id
    calcPrice(boat)
    db.session.commit()

def add_payment(current_page, form, boat, id):
    sanitize_paid_days = sanitize(form.paid_days.data)
    sanitize_paid_nights = sanitize(form.paid_nights.data)
    paid_enw = form.paid_enw.data
    paid_with = form.paid_with.data
    current_visit = None

    current_visit = Visit.query.get(id)

    current_visit.paid_days = sanitize_paid_days
    current_visit.paid_nights = sanitize_paid_nights
    current_visit.unpaid_days = 0
    current_visit.unpaid_nights = 0
    if paid_enw == "Yes":
        current_visit.paid_enw = True
    else:
        current_visit.paid_enw = False
    current_visit.paid_with = paid_with
    current_visit.date_paid = calc_current_time()
    calcPrice(boat)
    user = User.query.get(int(current_user.id))
    if current_visit.logged_by == None:
        current_visit.logged_by = user.id
    if current_visit.payment_by == None:
        current_visit.payment_by = user.id
    db.session.commit()
    flash("Successfully added payment!", category='success')

def add_visit(current_page, form, boat):
    sanitize_paid_days = sanitize(form.paid_days.data)
    sanitize_paid_nights = sanitize(form.paid_nights.data)
    paid_enw = form.paid_enw.data
    paid_with = form.paid_with.data
    current_visit = None

    current_visit = Visit()

    current_visit.paid_days = sanitize_paid_days
    current_visit.paid_nights = sanitize_paid_nights
    current_visit.unpaid_days = 0
    current_visit.unpaid_nights = 0
    if paid_enw == "Yes":
        current_visit.paid_enw = True
    else:
        current_visit.paid_enw = False
    current_visit.paid_with = paid_with
    current_visit.date_in = calc_current_time()
    current_visit.boat_id = boat.id
    print(current_visit)
    db.session.add(current_visit)
    calcPrice(boat)
    boat.latest_date_in = current_visit.date_in
    if current_visit.logged_by == None:
        user = User.query.get(int(current_user.id))
        current_visit.logged_by = user.id
    db.session.commit()

def remove_from_current_Visits(boat_id):
    boat = Boat.query.get(boat_id)
    if boat:
        boat.current_boats_id = None
        db.session.commit()
    else:
        print("Boat not found!")
        flash("Tried to remove boat from current boats that doesn't exist", category='error')
            
def remove_visit(visit_id):
    current_visit = Visit.query.get(int(visit_id))
    if current_visit:
        db.session.delete(current_visit)
        db.session.commit()
        flash("Visit deleted succesfully", category='success')
    else:
        flash("Tried to delete Visit that doesn't exists", category='error')

def delete_visit_from_boat(boat_id, visit_id):
    boat = getBoatById(boat_id)
    sorted_visits = sorted(boat.visits, key=sort_key, reverse=True)
    if len(boat.visits) > 1:
        remove_visit(visit_id)
        boat.latest_date_in = sorted_visits[0].date_in
    elif len(boat.visits) == 1:
        remove_visit(visit_id)
        boat.latest_date_in = None

def get_boat_phone_number(phone_number):
    results = list()
    sanitized_phone_number = sanitize(phone_number)
    #print(Boat.query.filter(Boat.sanitized_phone_number==sanitized_phone_number))
    results = Boat.query.filter(Boat.sanitized_phone_number==sanitized_phone_number).first()
    return results