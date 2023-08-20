import os
from flask import Flask, redirect, request, Blueprint

import stripe
# This is your test secret API key.

checkout = Blueprint('checkout', __name__)

stripe.api_key = 'sk_test_51NgydBFLI0YQxiReRUGcliWrU3V2a3VoRzzH0DIU4rUyJrWGNAWkzBfQ8SUQ5OsHna5ioy42uchhRLoJ2KoewiD8000KtpTA3N'

YOUR_DOMAIN = 'http://localhost:5000'

@checkout.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NgyjfFLI0YQxiReBfcOZ7Vp',
                    'quantity': 100,
                }, {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NgyjfFLI0YQxiReBfcOZ7Vp',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
            phone_number_collection={
                'enabled': True,
            },
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)