from .models import Boat
from flask import flash

def getBoatById(id):
    boat = Boat.query.get(id)
    if boat is None:
        flash('No boat with given ID found', 'error')
        return None
    else:
        return boat

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

