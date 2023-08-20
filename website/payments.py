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

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
      payment_method_types = payment_intent.get('payment_method_types', [])
      print(f"Payment Method Types: {payment_method_types}")
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)