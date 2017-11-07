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
                   User_Org, State,
                   connect_to_db, db)
from paypal_functions import generate_payment_object, api, client_id, client_secret


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

    return render_template('dashboard.html')


# Registration and login logic functions
###############################################################################


@app.route('/register')
def show_registration_form():
    """render registration form"""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_registration():
    """extract data from reg form, add user to database, redirect
    to donate page with login added to session"""

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

    user_object = User.query.filter(User.email == user_email).first()

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
    flash('successfully logged out...50-50 odds')
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
    org = Organization.query.filter(Organization.org_id == 1).one()
    return render_template('donate.html', org=org)


@app.route('/donated', methods=['POST'])
def process_donation():

    user_id = session['current_user']
    org_id = request.form.get('org')

    print "user_id=", user_id
    print "org_id=", org_id

    payment_object = generate_payment_object(user_id, org_id)

    ##Generate payment obj using payer info from session, org info from form

    ##generate Transaction object to go into db

    flash('I got redirected here from the paypal button!')
    return redirect('/dashboard', payment_object)




@app.route('/buttons')
def show_button_options():
    """shows all the buttons I've copied and pasted from paypal"""
    return render_template('donation-buttons.html')



@app.route('/process', methods=['POST'])
def process_payment():
    """processes payment"""

    paymentID = request.form.get('paymentID')


    flash('I think I just processed a payment')
    return redirect('/')





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
