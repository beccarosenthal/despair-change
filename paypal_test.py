from paypalrestsdk import Payment, configure
import os

client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")

api = configure({"mode": "sandbox",
                         "client_id": client_id,
                         "client_secret": client_secret})


# Create payment object
payment = Payment({
    "intent": "sale",

  # Set payment method
    "payer": {
      "payer_info": {"email": "beccarosenthal-buyer@gmail.com",
                     "first_name": "Becca",
                     "last_name": "Rosenthal",
                     },

      "payment_method": "paypal",
      },

      # Set redirect urls
      "redirect_urls": {
        "return_url": "/process",
        "cancel_url": "/cancel"
      },

      # Set transaction object
      "transactions": [{
        "amount": {
          "total": "10.00",
          "currency": "USD"
        },
        "description": "test donation",

        "payee": {
                  'email': "beccarosenthal-facilitator@gmail.com",
                  'payee_display_metadata':
                    {
                    'brand_name':
                    "This is an ORG"
                    },
                  },

      }
      ]
    })


# Create payment
if payment.create():
  # Extract redirect url
  for link in payment.links:
    if link.method == "REDIRECT":
      # Capture redirect url
      redirect_url = str(link.href)

      # REDIRECT USER to redirect_url
else:
  print("Error while creating payment:")
  print(payment.error)

##WHEN YOU GO TO THAT LINK< IT ACTUALLY WORKS


###payment is a dictionary, representing the transaction between person being paid and doing paying
  # Payment id obtained when creating the payment (following redirect)
payment = Payment.find("PAY-28103131SP722473WKFD7VGQ")

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
