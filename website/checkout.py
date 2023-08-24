import os
from flask import Flask, redirect, request, Blueprint, flash

import stripe
# This is your test secret API key.

checkout = Blueprint('checkout', __name__)

stripe.api_key = 'sk_test_51NgydBFLI0YQxiReRUGcliWrU3V2a3VoRzzH0DIU4rUyJrWGNAWkzBfQ8SUQ5OsHna5ioy42uchhRLoJ2KoewiD8000KtpTA3N'

YOUR_DOMAIN = 'http://localhost:5000'

@checkout.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    days = int(request.args.get('days', ''))
    nights = int(request.args.get('nights', ''))
    electric = bool(request.args.get('electric', ''))
    #Size can be "0-25", "26-40", "41-Over"
    size = request.args.get('size', '')
    boatid = request.args.get('id', '')
    print("days:", days)
    print("nights:", nights)
    print("electric:", electric)
    print("size:", size)
    print("boatid:", boatid)
    #Check size and add payments depending on q-strings to line items
    items = []
    if size == "0-25":
        #Checks electric
        if nights > 0:
            if electric:
                items.append(
                        {
                            'price': 'price_1NhisAFLI0YQxiReQV8RZaZ4',
                            'quantity': nights,
                            }
                    )
            else:
                items.append(
                        {
                            'price': 'price_1NhirUFLI0YQxiRep7QS1OBN',
                            'quantity': nights,
                            }
                    )
        
        #Checks day fee
        if days > 0:
            items.append(
            {
                'price': 'price_1NhiveFLI0YQxiReCDp42dal',
                'quantity': days,
                }
            )
      
    elif size == "26-40":
        #Checks electric
        if nights > 0:
            if electric:
                items.append(
                        {
                            'price': 'price_1NhistFLI0YQxiReCzXfIDMJ',
                            'quantity': nights,
                            }
                    )
            else:
                items.append(
                        {
                            'price': 'price_1NhisdFLI0YQxiReeEO2YF47',
                            'quantity': nights,
                            }
                    )
        
        #Checks day fee
        if days > 0:
            items.append(
            {
                'price': 'price_1Nhiw7FLI0YQxiRekPsBHYUa',
                'quantity': days,
                }
            )
           
    elif size == "41-Over":
        #Checks electric
        if nights > 0:
            if electric:
                items.append(
                        {
                            'price': 'price_1NhitUFLI0YQxiRetQzzLvTC',
                            'quantity': nights,
                            }
                    )
            else:
                items.append(
                        {
                            'price': 'price_1NhitJFLI0YQxiRegF7uPEhi',
                            'quantity': nights,
                            }
                    )
        
        #Checks day fee
        if days > 0:
            items.append(
            {
                'price': 'price_1NhiwRFLI0YQxiReLKPEPDnb',
                'quantity': days,
                }
            )

    print(items)
    #Creates checkout session with correct items
    if items:
        try:
            checkout_session = stripe.checkout.Session.create(
                #Sets what they are paying for
                line_items=items,
                mode='payment',
                invoice_creation={"enabled": True},

                #URL to redirect to if payment is success
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',

                #Add Boat ID to pass through stripe
                client_reference_id = boatid if boatid else None        
            )
        except Exception as e:
            return str(e)
        
        return redirect(checkout_session.url, code=303)
    else:
        print("No product items!!!")
        flash("ERROR add days and night fees")
        return redirect('cancel.hmtl')