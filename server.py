"""DESPAIR CHANGE"""
#python standard libraries
import datetime
import os

#third party things
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from paypalrestsdk import Payment, configure


#import from my files
from model import (User, Organization, Transaction,
                   UserOrg, State,
                   connect_to_db, db)
from paypal_functions import generate_payment_object, api


app = Flask(__name__)
app.secret_key = 'werewolf-bar-mitzvah'

client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")


# General templates
###############################################################################


@app.route('/')
def index():
    """renders homepage"""

    return render_template('homepage.html')


@app.route('/about')
def show_about_page():
    """renders about Despair Change page"""

    return render_template('about.html')


@app.route('/dashboard')
def show_user_dashboard():
    """show user dashboard"""

    current_user_id = session['current_user']
    user_object = User.query.filter(User.user_id == current_user_id).first()

    return render_template('dashboard.html', user=user_object)


# Registration and login logic functions
###############################################################################


@app.route('/register')
def show_registration_form():
    """render registration form"""

    #make sure that logged in user cannot see reg page
    if 'current_user' in session:
        return redirect('/')

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_registration():
    """extract data from reg form, add user to database, redirect
    to donate page with login added to session"""

    # *****TODO fix server.py logic so that user registering with
    # wrong password redirects them to login page
    if 'current_user' in session:
        print "***current user in session"
        import pdb; pdb.set_trace()
        return redirect('/login')

    #TODO add logic about making sure they type a password that matches -
    # it may be on the html template, not here
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    state = request.form.get('state')
    phone = request.form.get('phone')

    user_object = User.query.filter(User.user_email == user_email).first()
    password = user_object.password

    #If user object with email address provided doens't exist, add to db...
    if not user_object :
        new_user = User(user_email=user_email,
                        password=user_password,
                        fname=fname,
                        lname=lname,
                        age=age,
                        zipcode=zipcode,
                        state_code=state,
                        phone=phone)
        db.session.add(new_user)
        db.session.commit()

    session['current_user'] = user_object.user_id
    print session['current_user']
    return redirect('/login')


@app.route('/login')
def show_login_form():
    """render login form"""

    if 'current_user' in session:
        flash('You\'re already logged in...let\'s go make an impact!')
        return redirect('/donate')

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """process login form, redirect to donor page when it works"""

    #get form data
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    #get the user object from the email
    user_object = User.query.filter(User.user_email == user_email).first()

    if user_object:
    #check password against email address
        if user_object.password == user_password:

            #TODO make last login work
            # #update user.last_login in database
            # user_object.last_login = datetime.datetime.utcnow
            # db.session.commit()

            flash("You're logged in. Welcome to Despair Change!!")
            specific_user_id = user_object.user_id
            session['current_user'] = specific_user_id

            #What is the specific user ID
            return redirect('/donate')

        else:
            flash("That is an incorrect password")
            return redirect('/login')

    else:
        flash('You need to register first!')
        return redirect('/register.html')


@app.route('/logout')
def logout_user():
    """logs out user by deleting the current user from the session"""

    del session['current_user']
    flash('Successfully Logged Out')
    return redirect ('/')


@app.route('/cancel')
def cancel_payment():
    """cancels payment"""


    flash('I think I just canceled a payment')
    return redirect('/')


#routes about paypal/payment things
###############################################################################
@app.route('/donate')
def donation_page():
    """render page to donate"""

    #TODO - when project develops into multiple orgs, target_org-->list

    org = Organization.query.filter(Organization.name.like('Institute%')).first()

    return render_template('donate.html', org=org)


@app.route('/donated', methods=['POST'])
def process_donation():
    """FIGURE THIS OUT"""

    user_id = session['current_user']
    org_id = request.form.get('org')

    print "user_id=", user_id
    print "org_id=", org_id

    amount = User.query.get(user_id).default_amount
    #TODO change status=pending_delivery to donation attempted, change data model

    transaction = Transaction(org_id=org_id,
                              user_id=user_id,
                              payment_id="Unrequested",
                              amount=amount,
                              status="donation attempted"
                              )
    print "****transaction object built, prepared to be added to db"

    # import pdb; pdb.set_trace()

    db.session.add(transaction)
    db.session.commit()

    #generate the payment object using information from the database
    redirect_url, payment_object = generate_payment_object(user_id, org_id)
    import pdb; pdb.set_trace

    print redirect_url
    print "###############"
    print "#################"

    print "#################"
    print "#################"
    print
    print "back in /donated route. "
    print "here comes the payment object from the paypal_functions file"
    print payment_object

    # extract paypal id from paypal object
    paypal_id = payment_object.id

    #update transaction object in the database
    transaction.payment_id = paypal_id
    transaction.status = "paypal payment instantiated"
    db.session.commit()
    import pdb; pdb.set_trace()


    return redirect(redirect_url)
    ##At this point, it generates payment, redirects to paypal, invites me to log in.
    ##once i log in, it lets me donate a dollar, and completes the transfer from
    ##the buyer account to the facilitator account with paypal.
    ##it keeps me on the paypal test page instead of kicking me back to the /process
    ##route


#   Figure this part out
@app.route('/process', methods=['GET'])
def process_payment():
    """processes payment"""

    #If it's made it this far, the payment went through.
    #update transaction in the database
    paypal_id = request.args.get('paymentId')

    transaction = Transaction.query.all()[-1]

    transaction.status = "pending delivery to org"
    db.session.commit()

    print "I'm here!"

    # paymentID = request.form.get('paymentID')

    #TODO If we get here, figure out how to update transaction status

    flash('Payment successful')
    return redirect('/')


@app.route('/buttons')
def show_button_options():
    """shows all the buttons I've copied and pasted from paypal"""

    org = Organization.query.filter(Organization.name.like('Institute%')).first()

    return render_template('buttons.html', org=org)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
