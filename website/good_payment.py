from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import os
import stripe
from .payment_functions import boater_adds_payment
from .functions import getBoatById

good_payment = Blueprint('good_payment', __name__)

stripe.api_key = ""

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = ''

@good_payment.route('/success', methods=['GET'])
def success():
    #Session id from payment and set variables
    paid_items = []
    total = None
    session_id = request.args.get('session_id', '')
    boat = None

    #Gets session with id
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'],)

        #Get variables from json
        boat_id = checkout_session.client_reference_id

        #Get Checkout details like quantity 
        line_items = checkout_session.line_items
        
        paid_items = []
        for item in line_items:
            quantity = item.quantity
            description = item.description
            item_total = item.amount_total
            
            paid_item = {
                "quantity": quantity,
                "description": description,
                "item_total": item_total
            }
            
            paid_items.append(paid_item)
        total=checkout_session.amount_total
        print(paid_items)
        boat = getBoatById(boat_id)
        boater_adds_payment(paid_items, boat_id)
        print("Amount Total", total)
        print("Boat ID: ", boat_id) 
    except Exception as e:
        print(e)
    return render_template('success.html', paid_items=paid_items, amount_total=total, boat=boat)
