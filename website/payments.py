from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import os
import stripe

payments = Blueprint('payments', __name__)

stripe.api_key = ""

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = ''

@payments.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f"ValueError: {e}")
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"SignatureVerificationError: {e}")
        raise e

    if event['type'] == 'checkout.session.completed':
      payment_checkout = event['data']['object']
      customer_details = payment_checkout.get("customer_details", [])
      print(f"Customer Details: {customer_details}")
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
