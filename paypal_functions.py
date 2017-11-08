import os

from paypalrestsdk import Payment, configure

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

    user_obj = User.query.filter(User.user_id == user_id).one()
    org_obj = Organization.query.filter(Organization.org_id == org_id).one()

    #Generate Payment Object
        #TODO #Figure out how to make intent donate
    payment = Payment({
        "intent": "sale",

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
                "total": user_obj.default_amount,
                "currency": "USD"
                },
            "description": "Donation",

            #TODO make payee info come from db
            "payee": {
                      'email': org_obj.payee_email,
                      'payee_display_metadata':
                        {'brand_name': org_obj.name},
                      },

        }
        ]
        })

    print "###############"
    print "#################"
    print "here is the payment before it's gotten sent to paypal to become real"
    print payment
    print "#################"
    print "#################"


    #TODO transaction status to "payment object built"

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
            # import pdb; pdb.set_trace()

        return redirect_url, payment

            # REDIRECT USER to redirect_url
    else:
        print("Error while creating payment:")
        print(payment.error)

        #TODO Update Transaction status
        return("this didn't work", payment)


if __name__ == "__main__":
###payment is a dictionary, representing the transaction between person being paid and doing paying


    # Execute payment using payer_id obtained when creating the payment (following redirect)
    if payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):
      print("Payment[%s] execute successfully" % (payment.id))
    else:
      print(payment.error)


    from paypalrestsdk import Payment

    # Payment id obtained when creating the payment (following redirect)
    payment = Payment.find("PAY-28103131SP722473WKFD7VGQ")

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
