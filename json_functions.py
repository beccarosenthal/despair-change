from flask import Flask, redirect, request, session, jsonify
from sqlalchemy import func

from model import (User, Organization, Transaction,
                   UserOrg, State,
                   connect_to_db, db)
# from server import get_user_object_and_current_user_id

BACKGROUND_COLORS = ["#C72DB3", "#D9A622", "#2CA248", "#6574DA",
                     "#C72D2D", "#2DC7C0", "#FF6384", "#FEFF29", ]
HOVER_BACKGROUND_COLORS = ["#2DC7C0", "#FF6384", "#FEFF29","#000000",
                           "#36A2EB", "#FF00FF", "#6574DA", "#C72D2D",  ]

def json_user_impact_bar(user_object):
    #####THE VERSION I HAVE THAT MAKES 5 BARS SHOW UP IN ONE SPOT
    current_user_id = user_object.user_id

    #Create dictionary with key value pairs of {org_id: amt donated by user}
    users_donations = (db.session.query(func.sum(Transaction.amount),
                                                 Transaction.org_id)
                                 .filter(Transaction.user_id == current_user_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())

    # list of users referred by current user
    referred_by_user = []
    direct_referral = user_object.referred
    for user in direct_referral:
        referred_by_user.append(user.referred)



    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in users_donations}


    labels = [] #name of org
    data = [] #amount of money

    for org, amount in donations_by_org.items():
        labels.append(org[:30])
        data.append(amount)
    #####TODO Add datasets to correspond with the referrals and total donations
    ###and make those labels different on stacked
        ### 3 datasets - one for user, one for referrals, one for all users
        ### so that users can interactively show/get rid of the other info


    data_dict = {
                "labels": labels,
                "datasets": [
                    {   "label": ["My Donations"],
                        "data": data,
                        "backgroundColor": BACKGROUND_COLORS,
                        "hoverBackgroundColor": HOVER_BACKGROUND_COLORS
                    }]
            }

    return jsonify(data_dict)


#TODO #THIS DOESN"T WORK YET
def json_total_impact_bar():
    """generate data_dict with data for the total impact bar chart"""

    ##TODO: Figure out how to make the visual show up as each individual user stacked on top of
    ##each other
    all_donations = (db.session.query(func.sum(Transaction.amount),
                                               Transaction.org_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())



    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in all_donations}

    labels = [] #name of org
    data = [] #amount of money

    for org, amount in donations_by_org.items():
        labels.append(org[:30])
        data.append(amount)
    #####TODO Add datasets to correspond with the referrals and total donations
    ###and make those labels different on stacked
        ### 3 datasets - one for user, one for referrals, one for all users
        ### so that users can interactively show/get rid of the other info

    data_dict = {
                "labels": labels,
                "datasets": [
                    {   "label": ["Despair Change's Impact"],
                        "data": data,
                        "backgroundColor": BACKGROUND_COLORS,
                        "hoverBackgroundColor": HOVER_BACKGROUND_COLORS
                    }]
            }

    return jsonify(data_dict)
