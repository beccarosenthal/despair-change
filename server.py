"""deSPARE CHANGE"""


from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
# from model import User, Rating, Movie, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension

from paypalrestsdk import Payment, configure
import os

app = Flask(__name__)
app.secret_key = 'werewolf-bar-mitzvah'

client_id = os.environ.get("PAYPAL_CLIENT_ID")
client_secret = os.environ.get("PAYPAL_CLIENT_SECRET")

@app.route('/')
def index():
    """renders homepage"""

    return render_template('homepage.html')


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

    # do something to update the last time logged in into the User.last_login
    #while we don't have db up and running, let's just assume user logged in
    session['current_user'] = 'logged_in'

    # user_object = User.query.filter(User.email == user_email).first()
    # if user_object:

    #     if user_object.password == user_password:
    #         flash("You're logged in. Welcome to deSpare Change!!")
    #         specific_user_id = user_object.user_id
    #         session['current_user'] = specific_user_id

    #         #What is the specific user ID
    #         url = '/users/' + str(specific_user_id)
    #         return redirect(url)

    #     else:
    #         flash("That is an incorrect password")
    #         return redirect('/login')
    # else:
    #     flash('You need to register first!')
    flash('for now, we\'ll assume you\'re actually logged in')
    return redirect('/donate')


@app.route('/register')
def show_registration_form():
    """render registration form"""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def process_registration():
    """extract data from reg form, add user to database, redirect
    to donate page with login added to session"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    gender = request.form.get('gender')
    phone = request.form.get('phone')

    user_object = User.query.filter(User.email == user_email).first()

    session['current_user'] = user_email
    if user_object:
        return redirect('/login')
    #If user object with email address provided doens't exist, add to db...
    else:
        new_user = User(email=user_email,
                        password=user_password,
                        fname=fname,
                        lname=lname,
                        age=age,
                        zipcode=zipcode,
                        gender=gender,
                        phone=phone)
        db.session.add(new_user)
        db.session.commit()

    return redirect('/login')


@app.route('/about')
def show_about_page():
    """renders about page"""

    return render_template('about.html')



@app.route('/dashboard')
def show_user_dashboard():
    """show user dashboard"""

    return render_template('dashboard.html')


@app.route('/donate')
def donation_page():
    """render page to donate"""

    return render_template('donate.html')


@app.route('/donated', methods=['POST'])
def process_donation():


    flash('I got redirected here from the paypal button!')
    return redirect('/dashboard')

@app.route('/logout')
def logout_user():
    """logs out user by deleting the current user from the session"""

    del session['current_user']
    flash('successfully logged out...50-50 odds')
    return redirect ('/')


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


@app.route('/cancel')
def cancel_payment():
    """cancels payment"""


    flash('I think I just canceled a payment')
    return redirect('/')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
