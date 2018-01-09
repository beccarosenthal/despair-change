"""DESPAIR CHANGE"""
#python standard libraries
import datetime
import os
import random

#third party things
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify, g)
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from paypalrestsdk import Payment, configure, WebProfile
from sqlalchemy import func, desc
from uszipcode import ZipcodeSearchEngine


#import from my files
from helper_functions import get_current_transaction
from json_functions import (
                            json_org_donation_by_user,
                            json_org_donations_datetime,
                            json_stacked_user_impact_bar,
                            json_total_donations_line,
                            json_total_impact_bar,
                            json_user_impact_bar,
                            json_user_impact_donut,
                            get_all_referred_by_user,)

from model import (User, Organization, Transaction,
                   UserOrg, Referral, State,
                   connect_to_db, db)
from paypal_functions import (generate_payment_object, api, execute_payment,
                              generate_payment_object_referral)


app = Flask(__name__)
app.secret_key = 'werewolf-bar-mitzvah'

# PayPal app keys
client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")

# GoogleMaps Key
map_key = os.environ.get('GOOGLE_MAPS')

#jinja datetime formatting
@app.template_filter()
def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    """Custom Jinja filter to format dates consistently."""
    return value.strftime(format)

# General templates
###############################################################################
#to put object in g
@app.before_request
def do_this_before_each_request():

    if 'current_user' in session:
        user_obj = User.query.get(session['current_user'])
        g.user = user_obj
        if g.user: #without this, the site errors out in logout route
            g.orgs = user_obj.get_ranked_orgs()
        else:
            g.orgs = sorted(Organization.query.all(),
                key=lambda org: org.short_name)
    #decide if g.orgs is an else thing or not
    else:
        g.orgs = sorted(Organization.query.all(),
                key=lambda org: org.short_name)


@app.route('/')
def index():
    """renders homepage"""

    # $ Amount of attempted donations
    total_attempted = db.session.query(func.sum(Transaction.amount)).all()
    total_attempted = "$" +str(total_attempted[0][0]) + "0"

    #Get records of successful donations from db
    total_donated = (db.session.query(func.sum(Transaction.amount),
                                               Transaction.org_id)
                                .filter(Transaction.status == "pending delivery to org")
                                .group_by(Transaction.org_id)
                                .all())

    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in total_donated}

    total_amount = 0
    for key, amount in donations_by_org.items():
        total_amount += amount

    print donations_by_org
    print total_amount

    #Query for all transaction objects
    transactions = Transaction.query.order_by(desc(Transaction.timestamp)).all()
    #if a user is coming either from referrals or a new donor...
    if 'transaction' in session:
        transaction = Transaction.query.get(session['transaction'])
    else:
        transaction = None

    return render_template('homepage.html',
                           donations_by_org=donations_by_org,
                           total_amount=total_amount,
                           amount_attempted=total_attempted,
                           transaction=transaction,
                           transactions=transactions)


@app.route('/about')
def show_about_page():
    """renders about Despair Change page"""

    return render_template('about.html')


@app.route('/buttons')
def show_button_options():
    """shows all the buttons I've copied and pasted from paypal"""

    org = Organization.query.filter(Organization.name.like('Institute%')).first()

    return render_template('buttons.html', org=org)


@app.route('/welcome')
def show_welcome_page():
    """shows welcome page that donors who are not registered members get redirected to after donations"""

    if 'transaction' not in session:
        return redirect('/')

    # Get the user who just logged in
    transaction = Transaction.query.get(session['transaction'])
    session['transaction'] = transaction.transaction_id
    del session['transaction']

    transactions = (Transaction.query
                               .order_by(desc(Transaction.transaction_id))
                               .all())
    return render_template('welcome.html',
                           transaction=transaction,
                           transactions=transactions)

# Registration and login logic functions
###############################################################################
@app.route('/register')
def show_registration_form():
    """render registration form"""

    # Make sure that logged in user cannot see reg page
    if 'current_user' in session:
        return redirect('/')
    # Get all orgs and all states from DB to put on reg form
    orgs = Organization.query.all()
    states = State.query.all()

    return render_template('register.html', orgs=orgs, states=states)


@app.route('/register', methods=['POST'])
def process_registration():
    """extract data from reg form, add user to database, redirect
    to donate page with login added to session"""

    if 'current_user' in session:
        return redirect('/')

    user_email = request.form.get('email')

    # Run logic of encrypting password
    user_password = request.form.get('password')
    pw_hash = bcrypt.generate_password_hash(user_password, 10)

    fname = request.form.get('fname')
    lname = request.form.get('lname')

    # Set nullable things to db to None if not in user submit form
    age = request.form.get('age')
    if not age:
        age = None

    zipcode = request.form.get('zipcode')
    if not zipcode:
        zipcode = None

    state = request.form.get('state')
    if not state:
        state = None

    phone = request.form.get('phone')
    if not phone:
        phone = None

    user_object = User.query.filter(User.user_email == user_email).first()

    # If user object with email address provided doesn't exist, add to db...
    if not user_object :
        user_object = User(user_email=user_email,
                           password=pw_hash,
                           fname=fname,
                           lname=lname,
                           age=age,
                           zipcode=zipcode,
                           state_code=state,
                           phone=phone,
                           set_password=True)
        db.session.add(user_object)
        db.session.commit()

        # Now that there's a user obj, fill out their first favorite
        org_id = request.form.get('rank_1')
        if org_id:
            user_id = User.query.filter(User.user_email == user_email).first()
            new_user_org = UserOrg(user_id=user_id,
                                   org_id=org_id,
                                   rank=1)
            db.session.add(new_user_org)
            db.session.commit()

    # If user email existed in db and password is right, log them in

    if pw_hash == bcrypt.check_password_hash(user_object.password, user_password):
        session['current_user'] = user_object.user_id
        return redirect('/')

    # Make user sign in with correct password
    return redirect('/login')


@app.route('/login')
def show_login_form():
    """render login form"""

    if 'current_user' in session:
        return redirect('/')

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """process login form, redirect to donor page when it works"""

    # Get form data
    user_email = request.form.get('email')

    # Get the user object from the email
    user_object = User.query.filter(User.user_email == user_email).first()

    user_password = request.form.get('password')

    if user_object:
        if user_object.set_password == False:
            if user_object.transactions:
                session['transaction'] = user_object.transactions[-1].transaction_id
                return redirect('/welcome')

        # Check password against email address
        valid_password = bcrypt.check_password_hash(user_object.password, user_password)
        if valid_password:

            #TODO make last login work
            # #update user.last_login in database
            # user_object.last_login = datetime.datetime.utcnow
            # db.session.commit()

            flash("You're logged in. Welcome to Despair Change!!")
            session['current_user'] = user_object.user_id

            return redirect('/')

        else:
            flash("That is an incorrect password")
            return redirect('/login')

    else:
        flash('You need to register first!')
        return redirect('/register')


@app.route('/setup_password', methods=["POST"])
def setup_password():
    """allow users who have donated via referral or regular non-user donation to set their password"""

    print "in setup password"
    password = request.form.get("confirm_pass")
    pw_hash = bcrypt.generate_password_hash(password, 10)

    email = request.form.get("user_email")

    # They've made donation already, so the user is in the DB
    user = User.query.filter(User.user_email == email).first()
    user.password = pw_hash
    db.session.commit()

    session['current_user'] = user.user_id
    return redirect("/dashboard")


@app.route('/logout')
def logout_user():
    """logs out user by deleting the current user from the session"""

    session.clear()
    flash('Successfully Logged Out')
    return redirect ('/')


@app.route('/dashboard')
def show_user_dashboard():
    """show user dashboard"""

    user_obj, current_user_id = get_user_object_and_current_user_id()

    # Get total amount of money user has attempted to donate
    total_donated = (db.session.query(func.sum(Transaction.amount))
                               .filter(Transaction.user_id == current_user_id)
                               .first())

    # Create dictionary with key value pairs of {org: amt donated by user}
    donations_by_org = query_for_donations_by_org_dict(current_user_id)

    # Get info about user_org with rank #1 to generate referral url
    fave_orgs = user_obj.get_ranked_orgs()
    print "fave_orgs in show user dashboard fn ", fave_orgs
    if fave_orgs:
        print "inside the if statement"
        fave_org = fave_orgs[0]

    # If they don't have a #1, random org
    else:
        fave_org = random.choice(Organization.query.all())

    #Get list of all users included in footprint
    referred = get_all_referred_by_user(user_obj)
    user_and_footprint_objs = referred + [user_obj]
    footprint_transactions = []
    for user in user_and_footprint_objs:
        footprint_transactions.extend(user.transactions)

    ###GET AMOUNT OF MONEY GENERATED BY REFERRALS
    transactions = []
    for item in referred:
        transactions += item.transactions

    footprint_total = 0
    for transaction in transactions:
        footprint_total += transaction.amount

    return render_template('dashboard.html',
                           user=user_obj,
                           total_donated=total_donated[0],
                           donations_by_org=donations_by_org,
                           fave_org=fave_org,
                           footprint_transactions=footprint_transactions,
                           footprint_total=footprint_total)

@app.route("/settings")
def show_user_settings():
    """renders user settings form"""

    user_obj = User.query.filter(User.user_id == session['current_user']).first()

    all_orgs = Organization.query.all()

    # Get current favorite org for user
    current_faves = user_obj.get_ranked_orgs()

    print all_orgs
    return render_template("settings.html",
                           user_obj=user_obj,
                           orgs=all_orgs)


@app.route("/adjust_settings")
def change_user_settings():

    print "we're here!"

    user_id = session['current_user']
    user_obj = User.query.get(user_id)
    # Get the info for what org_id users designated for which rank
    rank_1 = request.args.get("rank_1")
    rank_2 = request.args.get("rank_2")
    rank_3 = request.args.get("rank_3")

    print "rank 1, 2, and 3"
    print rank_1, rank_2, rank_3
    print

    # Make sure user can only have 3 ranked orgs
    for i in range(1, 4):

        if request.args.get("rank_" + str(i)):
            rank = request.args.get("rank_" + str(i))

            # Do they already have a rank 1? if so, make it None, because it's getting replaced
            rank_at_i = (UserOrg.query.filter(UserOrg.user_id == user_id, UserOrg.rank == i).first())

            if rank_at_i:
                rank_at_i.rank = None
            # Do they already have a relationship between themselves and that org
            old_relationship = (UserOrg.query
                .filter(UserOrg.user_id == user_id, UserOrg.org_id == rank)
                .first())
            if old_relationship:
                old_relationship.rank = i
            else:
                new_user_org = UserOrg(user_id=user_id,
                                       org_id=rank,
                                       rank=i)
                db.session.add(new_user_org)

    new_default_amount = request.args.get("default_amount")
    print "new_default_amount:", new_default_amount

    # Update the database with new default amount
    if new_default_amount:
        user_obj.default_amount = int(new_default_amount)

    db.session.commit()

    return redirect("/dashboard")


# Routes about paypal/payment things
###############################################################################
@app.route('/donate')
def donation_page():
    """render page to donate"""

    if 'current_user' in session:
        user_id = session['current_user']
    # Get all org objects that user has designated as a favorite at any point
        orgs = User.query.get(user_id).get_ranked_orgs()

    else:
        orgs = Organization.query.all()

    return render_template('donate.html', orgs=orgs)


@app.route('/donated', methods=['POST'])
def process_donation():
    """handle user pressing a donate button"""
    #TODO change process donation route to account for users logged in or referred
    if "current_user" in session:
        user_id = session['current_user']

    org_id = request.form.get('org')
    amount = request.form.get('donation_amount')

    if not amount:
        amount = User.query.get(user_id).default_amount

    transaction = create_transaction_object(user_id, org_id, float(amount))

    # Generate the payment object using information from the database
    redirect_url, payment_object = generate_payment_object(user_id,
                                                           org_id, transaction)

    # Update transaction object in the database to add paypal's ID
    transaction.payment_id = payment_object.id
    transaction.status = "paypal payment instantiated"

    db.session.commit()

    return redirect(redirect_url)


@app.route('/donated/referred', methods=['GET'])
def do_referred_payment():
    """do the thing for payments with referrals"""

    #FOR TROUBLESHOOTING PURPOSES, LOG OUT whoever is in the session
    if 'current_user' in session:
        del session['current_user']

    print "in donated/referred"
    org_id = request.args.get("org_id")
    referrer_id = request.args.get("referrer_id")

    # Use the anonymous user ID to do the transaction
    user_id = User.query.filter(User.fname == "Anonymous").one().user_id

    #add referrer_id to the session so we can add the Referral
    session['referrer_id'] = int(referrer_id)

    transaction = create_transaction_object(user_id, org_id)

    # Generate the payment object using information from the database
    redirect_url, payment_object = generate_payment_object_referral(user_id,
                                                                    org_id, transaction)
    # Update transaction object in the database to add paypal's ID
    transaction.payment_id = payment_object.id
    transaction.status = "paypal payment instantiated"

    db.session.commit()

    return redirect(redirect_url)


@app.route('/donated/register', methods=['POST'])
def process_payment_new_user():
    """ Handle payment for visitor to the site without referral or account"""

    email = request.form.get('email')
    org_id = request.form.get('org')
    amount = request.form.get('donation_amount')
    if not amount:
        amount = 1.0

    # Check if that person has already made a donation
    user_obj = User.query.filter(User.user_email == email).first()

    if not user_obj:
        fname = "first_name"
        lname = "last_name"

        user_obj = User(user_email=email,
                        password=None,
                        fname=fname,
                        lname=lname,
                        set_password=False)

        db.session.add(user_obj)
        db.session.commit()

    transaction = create_transaction_object(user_obj.user_id,
                                            org_id,
                                            float(amount))

    # Generate the payment object using information from the database
    redirect_url, payment_object = generate_payment_object(user_obj.user_id,
                                                           org_id, transaction)

    # Update transaction object in the database to add paypal's ID
    transaction.payment_id = payment_object.id
    transaction.status = "paypal payment instantiated"

    db.session.commit()

    return redirect(redirect_url)


@app.route('/process', methods=['GET'])
def process_payment():
    """processes payment"""

    paypal_id = request.args.get('paymentId')

    # Get specific transaction out of DB
    transaction = (Transaction.query
                              .filter(Transaction.payment_id == paypal_id)
                              .first())


    # Payer ID is what PayPal uses to physically execute the payment
    payer_id = request.args.get('PayerID')

    # Get the payment object from the PayPal id
    payment = Payment.find(paypal_id)

    execute_payment(payer_id, payment, transaction)

    # If it's made it this far, the payment went through.
    if transaction.status == "payment succeeded":
        transaction.status = "pending delivery to org"
        db.session.commit()

    # If it's not a referral payment, go to the user dashboard
    session['just_donated'] = True

    org = Organization.query.get(transaction.org_id)
    user = User.query.get(transaction.user_id)

    if 'referrer_id' not in session:
        if transaction.user.fname == "first_name":
            user = process_non_user_donation(payment, transaction)
            flash("Congrats, {}! Your ${}0 donation to {} was successful!".format(
                user.fname, transaction.amount, org.name))
            session['transaction'] = transaction.transaction_id
            return redirect('/welcome')

        flash("Congrats, {}! Your ${}0 donation to {} was successful!".format(
                user.fname, transaction.amount, org.name))
        return redirect('/')

    else:
        user = process_referral(payment, transaction)
        flash("Congrats, {}! Your ${}0 donation to {} was successful!".format(
            user.fname, transaction.amount, org.name))
        session['transaction'] = transaction.transaction_id
        session['just_donated'] = True
        return redirect('/welcome')


def process_non_user_donation(paypal_payment, transaction):
    """ Process donation from non-user, change db accordingly"""

    payment_dict = paypal_payment.to_dict()

    payer_info = payment_dict['payer']['payer_info']

    email = payer_info.get('email')

    fname = payer_info.get('first_name')
    lname = payer_info.get('last_name')
    phone = payer_info.get('phone')

    #Update the information on the new user
    user_id = transaction.user.user_id
    user_obj = User.query.filter(User.user_email == email).first()

    user_obj.fname = fname
    user_obj.lname = lname
    if phone:
        user_obj.phone = phone

    db.session.commit()

    return user_obj


def process_referral(paypal_payment, transaction):
    """ Process referral payment and change database accordingly"""

    payment_dict = paypal_payment.to_dict()

    payer_info = payment_dict['payer']['payer_info']

    email = payer_info.get('email')

    # Get the user object for the user who made the payment (whether they knowingly signed up or not)
    referred_obj = User.query.filter(User.user_email == email).first()

    # If no Transactions have been made with that email address, add that user to the DB
    if not referred_obj or referred_obj.fname == "Anonymous" or referred_obj.fname == "first_name":

        fname = payer_info.get('first_name')
        lname = payer_info.get('last_name')
        phone = payer_info.get('phone')

        referred_obj = User(user_email=email,
                            password=None,
                            fname=fname,
                            lname=lname,
                            phone=phone,
                            set_password=False)

        db.session.add(referred_obj)
        db.session.commit()

    # Create a referral record in the database
    referrer_id = int(session['referrer_id'])
    referrals = Referral.query.all()

    # If the referred user doesn't already have a referrer in the database, add it
    if not referred_obj.referrer:

        referral = Referral(referrer_id=referrer_id,
                            referred_id=referred_obj.user_id)

        db.session.add(referral)
        db.session.commit()

    # Change the transaction's user_id so that it belongs to the person who made it
    transaction.user_id = referred_obj.user_id
    db.session.commit()

    del session['referrer_id']
    return referred_obj


@app.route('/cancel')
def cancel_payment():
    """cancels payment"""

    flash('I think I just canceled a payment')
    return redirect('/')


@app.route('/org/<specific_org_id>')
def display_org_page(specific_org_id):
    """display page about specific org"""

    specific_org = Organization.query.get(specific_org_id)

    return render_template('org.html', org=specific_org)



#Routes about Data vis
##############################################################################
@app.route('/stacked-user-impact-bar.json')
def stacked_user_impact_data():
    """Return bar chart data about user impact."""

    user_object, current_user_id = get_user_object_and_current_user_id()

    data_dict = json_stacked_user_impact_bar(user_object)
    return data_dict


@app.route('/user-impact-donut.json')
def user_impact_donut_data():
    """Return donut chart data about user impact."""

    user_object, current_user_id = get_user_object_and_current_user_id()

    data_dict = json_user_impact_donut(user_object)
    return data_dict

@app.route('/user-impact-bar.json')
def user_impact_data():
    """Return bar chart data about user impact."""

    user_object, current_user_id = get_user_object_and_current_user_id()

    data_dict = json_user_impact_bar(user_object)
    return data_dict


@app.route('/total-impact-bar.json')
def total_impact_data():
    """return bar chart data about collective impact of all users"""

    return json_total_impact_bar()


@app.route('/org-donut-chart.json')
def org_donut_chart():
    """get json object showing amount raised per user in donut chart"""

    #the idea is that it shows a lot of donors with small donations making up large donations
    pass

@app.route('/donations-over-time-line.json')
def timestamp_line_data():
    """return line chart data about times of donations by all users"""

    return json_total_donations_line()


@app.route('/stacked-org-bar.json')
def stacked_org_bar_data():
    """Return stacked bar chart data about daily donations by org"""

    return json_org_donations_datetime()



# POST HACKBRIGHT PLAYING WITH STUFF
############################################################################

@app.route('/map')
def show_map_demo():
    """show demo google map"""

    return render_template('map.html')


@app.route('/get_lat_long.json')
def zip_to_lat_long_json():
    """ given zipcode, return jsonified lat/long for googlemaps """

    # Get current user's zipcode
    if "current_user" in session:
        user_id = session['current_user']
        user = User.query.get(user_id)

        zipcode_string = user.zipcode

    # If no zipcode, marker will appear in Disneyland
    else:
        zipcode_string = '92802'

    # Changing type of zipcode string from unicode to string
    zipcode_string = str(zipcode_string)

    search = ZipcodeSearchEngine()
    zipcode_dict = search.by_zipcode(zipcode_string)

    lat = int(zipcode_dict['Latitude'])
    lng = int(zipcode_dict['Longitude'])

    lat_lon_dict = {'lat': lat, 'lng': lng}


    return jsonify(lat_lon_dict)


@app.route('/get_referral_zips.json')
def get_referral_zips():
    """ Get a list with all zip codes of all people in a user's referral chain
    """
    if "current_user" in session:
        user_id = session['current_user']
        user = User.query.get(user_id)

    referral_transactions = get_all_referred_by_user(user)
    zipcodes = set()
    lat_longs = {}

    for item in referral_transactions:
        print "item", item
        print "lat_longs", lat_longs
        print 'zipcodes', zipcodes
        if not item.zipcode:
            continue
        else:
            zipcode = item.zipcode

            search = ZipcodeSearchEngine()
            #dictionary of informatino pertaining to that zipcode, including lat/long
            zc_dict = search.by_zipcode(zipcode)

            if zipcode not in zipcodes:

                zipcodes.add(zc_dict['Zipcode'])
                lat = zc_dict['Latitude']
                lng = zc_dict['Longitude']
                lat_longs[zipcode] = {'lat': lat, 'lng': lng}

    print lat_longs
    return jsonify(lat_longs)

#HELPER FUNCTIONS
############################################################################
def create_transaction_object(user_id, org_id, amount=1.0):
    """create Transaction object for both referral and non referral transactions"""

    transaction = Transaction(org_id=org_id,
                              user_id=user_id,
                              payment_id="Unrequested",
                              amount=amount,
                              status="donation attempted"
                              )
    db.session.add(transaction)
    db.session.commit()

    return transaction
#Helper Functions with queries
##############################################################################

def get_user_object_and_current_user_id():
    """helper function to get user id out of session, return user object"""

    current_user_id = session['current_user']
    user_object = User.query.filter(User.user_id == current_user_id).first()

    return user_object, user_object.user_id


def query_for_donations_by_org_dict(user_id):
    """return dictionary of org name: amount donated by given user"""

    users_donations = (db.session.query(func.sum(Transaction.amount),
                                                 Transaction.org_id)
                                 .filter(Transaction.user_id == user_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())


    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in users_donations}

    return donations_by_org


def show_all_user_donations(user_id):
    """ Find all donations attempted by the user logged into the session"""

    total_donated = (db.session.query(func.sum(Transaction.amount))
                               .filter(Transaction.user_id == current_user_id,
                                       Transaction.status == "pending delivery to org")
                               .first())

    return total_donated


def get_current_faves(user_obj):
    """Takes user_id, returns list of users favorite orgs ordered by rank"""

    current_faves = (UserOrg.query
                            .filter(UserOrg.user_id == user_obj.user_id)
                            .order_by(UserOrg.rank)
                            .all())
    return current_faves


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)
    bcrypt = Bcrypt(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
