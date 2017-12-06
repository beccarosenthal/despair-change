# Despair Change

Despair Change is a full stack donation app that integrates PayPal's REST API to streamline the process of making micro-donations. With just a few clicks, people can donate to their favorite organizations, increase the footprint of their impact by referring their friends to do the same, and see stats, charts, and graphs that show their donations as a part of a larger sum of money. Registered users can change their default donation amounts, adjust which organization shows up front and center on the donation page, and see their donation history sorted by organization and date. Non registered users can make donations, through the app either directly or via referral link from a registered user. 

## Technologies Used

* Python
* Flask
* Flask SQLAlchemy
* Javascript/jQuery
* AJAX/JSON
* Jinja2
* PayPal REST API
* Chart.js
* HTML/CSS
* Bootstrap
* bcrypt


## Installation

To install Despair Change on your local machine, pip install -r requirements.txt. In order to make payments/process payments and interact with PayPal's REST API, you must source credentials from PayPal. 

## Usage

TODO: Write usage instructions

## Structure

* server.py Core of the Flask app; all routes
* model.py All database tables and class methods
* json_functions.py All queries and formatting of data for charts.js visuals
* paypal_functions.py All functions that communicate with the PayPal API and make the physical payments happen



## Next Steps

Version 2.0 will (hopefully) leave the sandbox and connect donors to real organizations and include more ways for users to customize what kind of data they see about donations made through Despair Change. 

## Author

Becca Rosenthal is a software engineer living in Oakland. 
