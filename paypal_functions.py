import os
import random
import string

from paypalrestsdk import Payment, configure, WebProfile

from model import (User, Organization, Transaction,
                   UserOrg, State,
                   connect_to_db, db)


client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")

api = configure({"mode": "sandbox",
                         "client_id": client_id,
                         "client_secret": client_secret})


#TODO figure out what needs to passed in in order to connect this to db
# Create payment object
def generate_payment_object(user_id, org_id):
    """generate payment object"""

    #TODO Write queries that will get info about the payer, payee, and transaction
    #from/for the database
    print "****in generate_payment_object function***"
    print
    user_obj = User.query.filter(User.user_id == user_id).one()
    org_obj = Organization.query.filter(Organization.org_id == org_id).one()

    current_transaction = (Transaction.query
                                      .order_by(Transaction.transaction_id)
                                      .all()[-1])



    # Name needs to be unique so just generating a random one
    wpn = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
    web_profile = WebProfile({
        "name": wpn,
        "presentation": {
            "brand_name": org_obj.name,
            "logo_image": org_obj.logo_url,
            "locale_code": "US"
        },
        "input_fields": {
            "allow_note": True,
            "no_shipping": 1,
            "address_override": 1
        },
        "flow_config": {
            "landing_page_type": "login",
            "bank_txn_pending_url": "http://localhost:5000/dashboard",

        }
        })
    if web_profile.create():
        print("Web Profile[%s] created successfully" % (web_profile.id))
    else:
        print(web_profile.error)
    #Generate Payment Object
    payment = Payment({
        "intent": "sale",
        "experience_profile_id": web_profile.id,
      # Set payment method
        "payer": {

            "payer_info": {"email": user_obj.user_email,
                         "first_name": user_obj.fname,
                         "last_name": user_obj.lname
                         },

            "payment_method": "paypal",
            },

        # Set redirect urls
        "redirect_urls": {
            "return_url": "http://localhost:5000/process",
            "cancel_url": "http://localhost:5000/cancel"
            },
      #TODO make connect this to db
      # Set transaction object
        "transactions": [{
            "amount": {
                #amount must be a string to be processed by paypal
                "total": str(user_obj.default_amount) + "0",
                "currency": "USD"
                },
            "description": "Donation to " + org_obj.name,

            #TODO make payee info come from db
            "payee": {
                      'email': org_obj.payee_email,
                      'payee_display_metadata':
                     {'brand_name': org_obj.name},
                      },

        }
        ]
        })

    # update transaction status in db
    current_transaction.status = "payment object built"
    db.session.commit()

    # import pdb; pdb.set_trace()
    # Create payment
    if payment.create():

        print "###############"
        print "#################"
        print "here is the payment after it's gotten sent to paypal to become real"
        print payment
        print "#################"
        print "#################"

        #TODO update transaction status (Potentially take from part in server.py
                                    #directly under #extract paypal id from object)

        # Extract redirect url
        for link in payment.links:
          if link.method == "REDIRECT":
            # Capture redirect url
            redirect_url = str(link.href)


            return redirect_url, payment

            # REDIRECT USER to redirect_url
    else:
        print("Error while creating payment:")
        current_transaction.status = "payment failed"
        print(payment.error)


        #TODO Update Transaction status
        return("this didn't work", payment)


def execute_payment(payer_id):
    """helper function to execute payments"""
    pass

if __name__ == "__main__":
###payment is a dictionary, representing the transaction between person being paid and doing paying

        # Execute payment using payer_id obtained when creating the payment (following redirect)
        # if payment.execute({"payer_id": payment['payer_id']}):
        #     print("Payment[%s] execute successfully" % (payment.id))
        # else:
        #     print(payment.error)

    # Execute payment using payer_id obtained when creating the payment (following redirect)
    if payment.execute():
      print("Payment[%s] execute successfully" % (payment.id))
    else:
      print(payment.error)


    from paypalrestsdk import Payment

    # Payment id obtained when creating the payment (following redirect)
    payment = Payment.find("PAY-1CR30319DP127223ALIFDRPI")

    # Execute payment using payer_id obtained when creating the payment (following redirect)
    if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):
      print("Payment[%s] execute successfully" % (payment.id))
    else:
      print(payment.error)


    # Payment id obtained when creating the payment (following redirect)
    payment = Payment.find("PAY-28103131SP722473WKFD7VGQ")

    # Execute payment using payer_id obtained when creating the payment (following redirect)
    if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):
      print("Payment[%s] execute successfully" % (payment.id))
    else:
      print(payment.error)
