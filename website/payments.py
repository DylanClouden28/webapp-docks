from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import os
import stripe

payments = Blueprint('payments', __name__)

stripe.api_key = "sk_test_51NgydBFLI0YQxiReRUGcliWrU3V2a3VoRzzH0DIU4rUyJrWGNAWkzBfQ8SUQ5OsHna5ioy42uchhRLoJ2KoewiD8000KtpTA3N"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_3fe49ac1502fb2910b856262e11429e8fabde90e6b5f68c6b96e02701f318700'

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