"""DESPAIR CHANGE"""
#python standard libraries
import datetime
import os

#third party things
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from paypalrestsdk import Payment, configure, WebProfile
from sqlalchemy import func


#import from my files
from json_functions import (json_user_impact_bar, json_user_impact_donut,
                            json_total_impact_bar)
from model import (User, Organization, Transaction,
                   UserOrg, State,
                   connect_to_db, db)
from paypal_functions import generate_payment_object, api, execute_payment


app = Flask(__name__)
app.secret_key = 'werewolf-bar-mitzvah'

client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")


# General templates
###############################################################################


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
    user_password = request.form.get('password')
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

    #If user object with email address provided doens't exist, add to db...
    if not user_object :
        user_object = User(user_email=user_email,
                           password=user_password,
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
    if user_password == user_object.password:
        session['current_user'] = user_object.user_id
        print session['current_user']
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

    del session['current_user']
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

    # donations = {}
    # for amount, org_id in total_donated_by_org:
    #     org_name = Organization.query.get(org_id).name
    #     donations[org_name] = amount

    #Create dictionary with key value pairs of {org: amt donated by user}
    donations_by_org = query_for_donations_by_org_dict(current_user_id)


    #TODO use regex to make total donated and amounts look like dollar amounts
    print total_donated
    return render_template('dashboard.html',
                           user=user_object,
                           total_donated=total_donated[0],
                           donations_by_org=donations_by_org)

@app.route("/settings")
def show_user_settings():
    """renders user settings form"""

    user_obj = User.query.filter(User.user_id == session['current_user']).first()

    all_orgs = Organization.query.all()
    current_faves = (UserOrg.query
                            .filter(UserOrg.user_id == user_obj.user_id)
                            .order_by(UserOrg.rank)
                            .all())

    ##If you have a current #1, it is ___. Would you like to change it? What would you like to be your 2 /3 spots

    print all_orgs
    return render_template("settings.html",
                           user_obj=user_obj,
                           orgs=all_orgs,
                           current_faves=current_faves)


@app.route("/adjust_settings")
def change_user_settings():

    print "we're here!"

    user_id = session['current_user']
    ##Get the info for what org_id users designated for which rank
    rank_1 = request.args.get("rank_1")
    rank_2 = request.args.get("rank_2")
    rank_3= request.args.get("rank_3")

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

        db.session.commit()


    return redirect("/dashboard")


#routes about paypal/payment things
###############################################################################
@app.route('/donate')
def donation_page():
    """render page to donate"""

    user_id = session['current_user']
    #get all org objects that user has designated as a favorite at any point
    fave_orgs = (Organization.query
                             .join(UserOrg, Organization.org_id == UserOrg.org_id)
                             .filter(UserOrg.user_id == user_id)
                             .order_by(UserOrg.rank)
                             .all())

    # If user doesn't have any UserOrgs, send over the whole org list

    # if not fave_org_id:
    fave_org_ids = [org.org_id for org in fave_orgs]
    #SQL Alchemy syntax to get all orgs whose id are not in fave_org_ids
    other_orgs = Organization.query.filter(~Organization.org_id.in_(fave_org_ids)).all()

    #create list with fave orgs at beginning, other orgs below
    orgs = fave_orgs + other_orgs

    return render_template('donate.html', orgs=orgs)


@app.route('/donated', methods=['POST'])
def process_donation():
    """FIGURE THIS OUT"""

    user_id = session['current_user']
    org_id = request.form.get('org')

    print "user_id=", user_id
    print "org_id=", org_id

    amount = User.query.get(user_id).default_amount

    #TODO Use regex to get amount to be a string format that paypal can take
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
    redirect_url, payment_object = generate_payment_object(user_id,
                                                           org_id)

    #update transaction object in the database to add paypal's ID
    transaction.payment_id = payment_object.id
    transaction.status = "paypal payment instantiated"

    # import pdb; pdb.set_trace()
    db.session.commit()

    return redirect(redirect_url)


#   Figure this part out
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

    return redirect('/dashboard')


@app.route('/cancel')
def cancel_payment():
    """cancels payment"""

    flash('I think I just canceled a payment')
    return redirect('/')
#Routes about Data vis
##############################################################################
@app.route('/user-impact-donut.json')
def user_impact_donut_data():
    """Return data about user impact."""

    user_object, current_user_id = get_user_object_and_current_user_id()
    data_dict = json_user_impact_donut(user_object)
    print data_dict

    return jsonify(data_dict)


@app.route('/user-impact-bar.json')
def user_impact_data():
    """Return bar chart data about user impact."""


# #####THE VERSION I HAVE THAT MAKES 5 BARS SHOW UP IN ONE SPOT
    user_object, current_user_id = get_user_object_and_current_user_id()

#     # find all donations attempted by the user logged into the session
#     total_donated = (db.session.query(func.sum(Transaction.amount))
#                                .filter(Transaction.user_id == current_user_id)
#                                .first())

#     #Create dictionary with key value pairs of {org_id: amt donated by user}
#     donations_by_org = query_for_donations_by_org_dict(current_user_id)

#     labels = [] #name of org
#     data = [] #amount of money
#     BACKGROUND_COLORS = ["#FF6384", "#36A2EB", "#FF6384", "#36A2EB",
#                          "#FF6384", "#36A2EB", "#FF6384", "#36A2EB", ]
#     HOVER_BACKGROUND_COLORS = ["#FF6384", "#36A2EB", "#FF6384", "#36A2EB",
#                               "#FF6384", "#36A2EB", "#FF6384", "#36A2EB"]
#     datasets = []
#     # datasets = [{"label": labels,
#     #              "data": data,
#     #              "backgroundColor": ["red", "blue"],
#     #              "hoverBackgroundColor": ["black", "grey"]}]

#     for org, amount in donations_by_org.items():
#         labels.append(org)
#         data.append(amount)

#     for i in range(len(data)):
#         datasets.append({
#                        "label": labels[i],
#                        "data": [data[i]],
#                        "backgroundColor": BACKGROUND_COLORS[i],
#                        "hoverBackgroundColor": HOVER_BACKGROUND_COLORS[i]
#                        },)
#         print datasets
#         # import pdb; pdb.set_trace()

#     data_dict = {
#                 "labels": labels,
#                 "datasets": datasets
#             }
#     print
#     print
#     print "$$$$$$DATADICT"
#     print data_dict
#     print
#     print
#     print "$$$$$$DATASETS"
#     print datasets

    data_dict = json_user_impact_bar(user_object)
    return jsonify(data_dict)


@app.route('/total-impact-bar.json')
def total_impact_data():
    """return bar chart data about collective impact of all users"""

    # all_donations = (db.session.query(func.sum(Transaction.amount),
    #                                            Transaction.org_id)
    #                              .filter(Transaction.status == "pending delivery to org")
    #                              .group_by(Transaction.org_id)
    #                              .all())

    # # import pdb; pdb.set_trace()
    # print "figure out what all donations is"
    # labels = []
    # data = []

    # for org, amount in all_donations.items():
    #     labels.append(org)
    #     data.append(amount)

    # data_dict = {
    #             "labels": labels,
    #             "datasets": [
    #                 {
    #                     "data": data,
    #                     "backgroundColor": [
    #                         "#FF6384",
    #                         "#36A2EB",
    #                     ],
    #                     "hoverBackgroundColor": [
    #                         "#FF6384",
    #                         "#36A2EB",
    #                     ]
    #                 }]
    #         }
    data_dict = json_total_impact_bar()
    return jsonify(data_dict)


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


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
