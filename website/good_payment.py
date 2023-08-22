from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import os
import stripe

good_payment = Blueprint('good_payment', __name__)

stripe.api_key = "sk_test_51NgydBFLI0YQxiReRUGcliWrU3V2a3VoRzzH0DIU4rUyJrWGNAWkzBfQ8SUQ5OsHna5ioy42uchhRLoJ2KoewiD8000KtpTA3N"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_3fe49ac1502fb2910b856262e11429e8fabde90e6b5f68c6b96e02701f318700'

@good_payment.route('/success', methods=['GET'])
def success():
    #Session id from payment and set variables
    paid_items = []
    total = None
    session_id = request.args.get('session_id', '')

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
        print("Amount Total", total)
        print("Boat ID: ", boat_id) 
    except Exception as e:
        print(e)
        flash("INVALID SESSION ID", category='error')
    return render_template('success.html', paid_items=paid_items, amount_total=total)