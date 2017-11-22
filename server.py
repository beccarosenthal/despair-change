"""DESPAIR CHANGE"""
#python standard libraries
import datetime
import os
import random

#third party things
# import Bcrypt
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify, g)
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from paypalrestsdk import Payment, configure, WebProfile
from sqlalchemy import func


#import from my files
from helper_functions import get_current_transaction
from json_functions import (json_user_impact_bar,
                            json_total_impact_bar,
                            json_stacked_user_impact_bar)
from model import (User, Organization, Transaction,
                   UserOrg, Referral, State,
                   connect_to_db, db)
from paypal_functions import (generate_payment_object, api, execute_payment,
                              generate_payment_object_referral)


app = Flask(__name__)
app.secret_key = 'werewolf-bar-mitzvah'

client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")



# General templates
###############################################################################
#to put object in g
@app.before_request
def do_this_before_each_request():
    if 'current_user' in session:
        user_obj = User.query.get(session['current_user'])
        g.user = user_obj
        g.orgs = user_obj.get_ranked_orgs()
    #decide if g.orgs is an else thing or not
    else:
        g.orgs = Organization.query.all()


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
    return render_template('homepage.html',
                           donations_by_org=donations_by_org,
                           total_amount=total_amount,
                           amount_attempted=total_attempted)


@app.route('/about')
def show_about_page():
    """renders about Despair Change page"""

    return render_template('about.html')


@app.route('/buttons')
def show_button_options():
    """shows all the buttons I've copied and pasted from paypal"""

    org = Organization.query.filter(Organization.name.like('Institute%')).first()

    return render_template('buttons.html', org=org)


# Registration and login logic functions
###############################################################################
@app.route('/register')
def show_registration_form():
    """render registration form"""

    #make sure that logged in user cannot see reg page
    if 'current_user' in session:
        return redirect('/')
    #Get all orgs and all states from DB to put on reg form
    orgs = Organization.query.all()
    states = State.query.all()

    return render_template('register.html', orgs=orgs, states=states)


@app.route('/register', methods=['POST'])
def process_registration():
    """extract data from reg form, add user to database, redirect
    to donate page with login added to session"""

    # *****TODO fix server.py logic so that user registering with
    # wrong password redirects them to login page
    if 'current_user' in session:
        print "***current user in session"
        return redirect('/')

    user_email = request.form.get('email')

    #run logic of encrypting password
    user_password = request.form.get('password')
    pw_hash = bcrypt.generate_password_hash(user_password, 10)

    fname = request.form.get('fname')
    lname = request.form.get('lname')

    # set nullable things to db to None if not in user submit form
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

    #If user object with email address provided doesn't exist, add to db...
    if not user_object :
        user_object = User(user_email=user_email,
                           password=pw_hash,
                           fname=fname,
                           lname=lname,
                           age=age,
                           zipcode=zipcode,
                           state_code=state,
                           phone=phone)
        db.session.add(user_object)
        db.session.commit()

        #now that there's a user obj, fill out their first favorite
        org_id = request.form.get('rank_1')
        if org_id:
            user_id = User.query.filter(User.user_email == user_email).first()
            new_user_org = UserOrg(user_id=user_id,
                                   org_id=org_id,
                                   rank=1)
            db.session.add(new_user_org)
            db.session.commit()

    #if user email existed in db and password is right, log them in

    if pw_hash == bcrypt.check_password_hash(user_object.password, user_password):
        session['current_user'] = user_object.user_id
        #They already logged in; send them to the donate page
        return redirect('/donate')

    # Make user sign in with correct password
    return redirect('/login')


@app.route('/login')
def show_login_form():
    """render login form"""

    if 'current_user' in session:
        return redirect('/donate')

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_user():
    """process login form, redirect to donor page when it works"""

    #get form data
    user_email = request.form.get('email')

    #get the user object from the email
    user_object = User.query.filter(User.user_email == user_email).first()

    user_password = request.form.get('password')
    valid_password = bcrypt.check_password_hash(user_object.password, user_password)

    if user_object:
    #check password against email address
        if valid_password:

            #TODO make last login work
            # #update user.last_login in database
            # user_object.last_login = datetime.datetime.utcnow
            # db.session.commit()

            flash("You're logged in. Welcome to Despair Change!!")
            session['current_user'] = user_object.user_id

            #What is the specific user ID
            return redirect('/donate')

        else:
            flash("That is an incorrect password")
            return redirect('/login')

    else:
        flash('You need to register first!')
        return redirect('/register')


@app.route('/logout')
def logout_user():
    """logs out user by deleting the current user from the session"""

    session.clear()
    flash('Successfully Logged Out')
    return redirect ('/')


@app.route('/dashboard')
def show_user_dashboard():
    """show user dashboard"""

    user_object, current_user_id = get_user_object_and_current_user_id()

    #get total amount of money user has attempted to donate
    total_donated = (db.session.query(func.sum(Transaction.amount))
                               .filter(Transaction.user_id == current_user_id)
                               .first())

    #Create dictionary with key value pairs of {org: amt donated by user}
    donations_by_org = query_for_donations_by_org_dict(current_user_id)

    #Get info about user_org with rank #1 to generate referral url
    fave_orgs = get_current_faves(user_object)
    print "fave_orgs in show user dashboard fn ", fave_orgs
    if fave_orgs:
        print "inside the if statement"
        fave_org = fave_orgs[0]

    #if they don't have a #1, whatever they gave to last time
    else:
        fave_org = random.choice(Organization.query.all())

    #TODO use regex to make total donated and amounts look like dollar amounts
    print donations_by_org
    return render_template('dashboard.html',
                           user=user_object,
                           total_donated=total_donated[0],
                           donations_by_org=donations_by_org,
                           fave_org=fave_org)

@app.route("/settings")
def show_user_settings():
    """renders user settings form"""

    user_obj = User.query.filter(User.user_id == session['current_user']).first()

    all_orgs = Organization.query.all()

    ##Get current favorite org for user
    current_faves = get_current_faves(user_obj)
    for fave in current_faves:
        print fave.org_id, fave.rank

    ##If you have a current #1, it is ___. Would you like to change it? What would you like to be your 2 /3 spots

    print all_orgs
    return render_template("settings.html",
                           user_obj=user_obj,
                           orgs=all_orgs)


@app.route("/adjust_settings")
def change_user_settings():

    print "we're here!"

    user_id = session['current_user']
    user_obj = User.query.get(user_id)
    ##Get the info for what org_id users designated for which rank
    rank_1 = request.args.get("rank_1")
    rank_2 = request.args.get("rank_2")
    rank_3 = request.args.get("rank_3")

    print "rank 1, 2, and 3"
    print rank_1, rank_2, rank_3
    print


    for i in range(1, 4):

        if request.args.get("rank_" + str(i)):
            rank = request.args.get("rank_" + str(i))

            #do they already have a rank 1? if so, make it None, because it's getting replaced
            rank_at_i = (UserOrg.query.filter(UserOrg.user_id == user_id, UserOrg.rank == i).first())

            if rank_at_i:
                rank_at_i.rank = None
            #do they already have a relationship between themselves and that org
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

    print "check datatypes on default amount old and new"
    import pdb; pdb.set_trace()

    if new_default_amount:
        user_obj.default_amount = int(new_default_amount)

    db.session.commit()
    print "make sure user_org and default amount changed in db"
    import pdb; pdb.set_trace()

    return redirect("/dashboard")


#routes about paypal/payment things
###############################################################################
@app.route('/donate')
def donation_page():
    """render page to donate"""

    if 'current_user' in session:
        user_id = session['current_user']
    #get all org objects that user has designated as a favorite at any point
        orgs = User.query.get(user_id).get_ranked_orgs()

    else:
        orgs = Organization.query.all()

    return render_template('donate.html', orgs=orgs)


@app.route('/donated', methods=['POST'])
def process_donation():
    """handle user pressing the donate button"""
    #TODO change process donation route to account for users logged in or referred
    if "current_user" in session:
        user_id = session['current_user']
    else:
        user_id = User.query.filter(User.fname == "Anonymous").first()
    org_id = request.form.get('org')
    amount = request.form.get('donation_amount')

    print "user_id=", user_id
    print "org_id=", org_id
    if not amount:
        amount = User.query.get(user_id).default_amount
    import pdb; pdb.set_trace()
    #TODO Use regex to get amount to be a string format that paypal can take
    transaction = create_transaction_object(user_id, org_id, amount)

    print "****transaction object built, added to db"

    #generate the payment object using information from the database
    redirect_url, payment_object = generate_payment_object(user_id,
                                                           org_id)

    #update transaction object in the database to add paypal's ID
    transaction.payment_id = payment_object.id
    transaction.status = "paypal payment instantiated"

    # import pdb; pdb.set_trace()
    db.session.commit()

    return redirect(redirect_url)


#   Figure this part out

@app.route('/donated/referred', methods=['GET'])
def do_referred_payment():
    """do the thing for payments with referrals"""

    #FOR TROUBLESHOOTING PURPOSES, LOG OUT whoever is in the session
    if 'current_user' in session:
        del session['current_user']

    print "in donated/referred"
    org_id = request.args.get("org_id")
    referrer_id = request.args.get("referrer_id")
    #FIXME referrer 27 is the anonymous user
    if not referrer_id:
        referrer_id = 27

    print org_id, "org id from url"
    print referrer_id, "referrer id from url"

    #TODO Instead of doing the whole thing with an anonymous user, instanciate new user right here
    user_id = User.query.filter(User.fname == "Anonymous").one().user_id
    print user_id, "user_id"

    #add referrer_id to the session so we can add the Referral
    session['referrer_id'] = int(referrer_id)

    transaction = create_transaction_object(user_id, org_id)

    #generate the payment object using information from the database
    redirect_url, payment_object = generate_payment_object_referral(user_id,
                                                                    org_id)
    #update transaction object in the database to add paypal's ID
    transaction.payment_id = payment_object.id
    transaction.status = "paypal payment instantiated"

    # import pdb; pdb.set_trace()
    db.session.commit()

    return redirect(redirect_url)

@app.route('/donated/register', methods=['POST'])
def process_payment_new_user():
    """handle payment for visitor to the site without referral or account"""
    amount = request.form.get('donation_amount')
    print amount

    import pdb; pdb.set_trace()
@app.route('/process', methods=['GET'])
def process_payment():
    """processes payment"""

    paypal_id = request.args.get('paymentId')

    #Get specific transaction out of DB
    transaction = (Transaction.query
                              .filter(Transaction.payment_id == paypal_id)
                              .first())

    print transaction.status

    print "check dashboard to see progress of payment to figure out how to update status"

    #payer ID paypal uses to physically execute the payment
    payer_id = request.args.get('PayerID')

    #Find the payment object from the paypal id
    payment = Payment.find(paypal_id)

    execute_payment(payer_id, payment, transaction)

    #If it's made it this far, the payment went through.
    if transaction.status == "payment succeeded":
        print "Money is in my hands, ready to be delivered to the org"
        transaction.status = "pending delivery to org"
        db.session.commit()

    #if it's not a referral payment, go to the user dashboard
    if 'referrer_id' not in session:
        return redirect('/dashboard')

    else:
        process_referral(payment, transaction)
        return redirect('/')


def process_referral(paypal_payment, transaction):
    """process referral payment and change database accordingly"""

    print "in process referral"

    payment_dict = paypal_payment.to_dict()

    payer_info = payment_dict['payer']['payer_info']

    email = payer_info.get('email')

    #Get the user object for the user who made the payment (whether they knowingly signed up or not)
    referred_obj = User.query.filter(User.user_email == email).first()

    #If no Transactions have been made with that email address, add that user to the DB
    if not referred_obj:

        fname = payer_info.get('first_name')
        lname = payer_info.get('last_name')
        phone = payer_info.get('phone')
        user_password = os.environ.get("DEFAULT_PASSWORD")
        pw_hash = bcrypt.generate_password_hash(user_password, 10)

        referred_obj = User(user_email=email,
                             password=pw_hash,
                             fname=fname,
                             lname=lname)

        db.session.add(referred_obj)
        db.session.commit()

    #change the transaction's user_id so that it belongs to the person who made it
    transaction.user_id = referred_obj.user_id
    db.session.commit()

    # Create a referral record in the database
    referrer_id = int(session['referrer_id'])
    referrals = Referral.query.all()

    #If the referred user doesn't already have a referrer in the database, add it
    if not referred_obj.referrer:

        referral = Referral(referrer_id=referrer_id,
                            referred_id=referred_obj.user_id)

        db.session.add(referral)
        db.session.commit()

    del session['referrer_id']

    flash("Welcome to Despair Change. Change your password, and you can start making an even bigger impact!")
    #FIXME this wants to process the paypal url, not the process thing

@app.route('/cancel')
def cancel_payment():
    """cancels payment"""

    flash('I think I just canceled a payment')
    return redirect('/')
#Routes about Data vis
##############################################################################
@app.route('/stacked-user-impact-bar.json')
def stacked_user_impact_data():
    """Return bar chart data about user impact."""

    user_object, current_user_id = get_user_object_and_current_user_id()

    data_dict = json_stacked_user_impact_bar(user_object)
    return data_dict


@app.route('/user-impact-bar.json')
def user_impact_data():
    """Return bar chart data about user impact."""

    user_object, current_user_id = get_user_object_and_current_user_id()

    data_dict = json_user_impact_bar(user_object)
    return data_dict


#TODO - this
@app.route('/total-impact-bar.json')
def total_impact_data():
    """return bar chart data about collective impact of all users"""

    return json_total_impact_bar()


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

    print "Transaction added to db"
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
    #find all donations that were successful
    #todo fix this query to include Transaction.status = "delivered to org"


    users_donations = (db.session.query(func.sum(Transaction.amount),
                                                 Transaction.org_id)
                                 .filter(Transaction.user_id == user_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())


    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in users_donations}

    return donations_by_org


#not sure if this works or not...
def show_all_user_donations(user_id):
    """find all donations attempted by the user logged into the session"""
    total_donated = (db.session.query(func.sum(Transaction.amount))
                               .filter(Transaction.user_id == current_user_id,
                                       Transaction.status == "pending delivery to org")
                               .first())

    return total_donated


def get_current_faves(user_obj):
    """takes user_id, returns list of users favorite orgs ordered by rank"""

    print user_obj
    current_faves = (UserOrg.query
                            .filter(UserOrg.user_id == user_obj.user_id)
                            .order_by(UserOrg.rank)
                            .all())
    print "current faves in get current faves function"
    print current_faves
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
