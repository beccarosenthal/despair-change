from flask import Flask, redirect, request, session
from sqlalchemy import func

from model import (User, Organization, Transaction,
                   UserOrg, State,
                   connect_to_db, db)
# from server import get_user_object_and_current_user_id

BACKGROUND_COLORS = ["#C72DB3", "#36A2EB", "#FF00FF", "#6574DA",
                     "#C72D2D", "#2DC7C0", "#FF6384", "#FEFF29", ]
HOVER_BACKGROUND_COLORS = ["#C72DB3", "#36A2EB", "#FF00FF", "#6574DA",
                     "#C72D2D", "#2DC7C0", "#FF6384", "#FEFF29", ]

def json_user_impact_bar(user_object):
    #####THE VERSION I HAVE THAT MAKES 5 BARS SHOW UP IN ONE SPOT
    current_user_id = user_object.user_id

    # find all donations attempted by the user logged into the session
    total_donated = (db.session.query(func.sum(Transaction.amount))
                               .filter(Transaction.user_id == current_user_id)
                               .first())

    #Create dictionary with key value pairs of {org_id: amt donated by user}
    #Create dictionary with key value pairs of {org_id: amt donated by user}
    users_donations = (db.session.query(func.sum(Transaction.amount),
                                                 Transaction.org_id)
                                 .filter(Transaction.user_id == current_user_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())


    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in users_donations}

    ### 3 datasets - one for user, one for referrals, one for all users


    labels = [] #name of org
    data = [] #amount of money

    for org, amount in donations_by_org.items():
        labels.append(org[:30])
        data.append(amount)
    #####TODO Add datasets to correspond with the referrals and total donations
    ###and make those labels different on stacked

    # datasets = []
    # # datasets = [{"label": labels,
    # #              "data": data,
    # #              "backgroundColor": ["red", "blue"],
    # #              "hoverBackgroundColor": ["black", "grey"]}]

    # for org, amount in donations_by_org.items():
    #     labels.append(org)
    #     data.append(amount)

    # for i in range(len(data)):
    #     datasets.append({
    #                    "label": labels[i],
    #                    "data": data[i],
    #                    "backgroundColor": BACKGROUND_COLORS[i],
    #                    "hoverBackgroundColor": HOVER_BACKGROUND_COLORS[i]
    #                    },)
    #     print datasets
    #     # import pdb; pdb.set_trace()


    data_dict = {
                "labels": labels,
                "datasets": [
                    {   "label": ["My Donations"],
                        "data": data,
                        "backgroundColor": BACKGROUND_COLORS,
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                        ]
                    }]
            }
    return data_dict


def json_user_impact_donut(user_object):
    """Return data about user impact for donut chart"""

    current_user_id = user_object.user_id

    # find all donations attempted by the user logged into the session
    total_donated = (db.session.query(func.sum(Transaction.amount))
                               .filter(Transaction.user_id == current_user_id)
                               .first())

    #Create dictionary with key value pairs of {org_id: amt donated by user}
    users_donations = (db.session.query(func.sum(Transaction.amount),
                                                 Transaction.org_id)
                                 .filter(Transaction.user_id == current_user_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())


    donations_by_org = {Organization.query.get(org_id).name: amount
                        for amount, org_id in users_donations}


    labels = []
    data = []

    for org, amount in donations_by_org.items():
        labels.append(org)
        data.append(amount)

    data_dict = {
                "labels": labels,
                "datasets": [
                    {
                        "data": data,
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                        ],
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                        ]
                    }]
            }
    return data_dict

def json_total_impact_bar():
    """generate data_dict with data for the total impact bar chart"""
    all_donations = (db.session.query(func.sum(Transaction.amount),
                                               Transaction.org_id)
                                 .filter(Transaction.status == "pending delivery to org")
                                 .group_by(Transaction.org_id)
                                 .all())

    # import pdb; pdb.set_trace()
    print "figure out what all donations is"
    labels = []
    data = []

    for org, amount in all_donations.items():
        labels.append(org)
        data.append(amount)

    data_dict = {
                "labels": labels,
                "datasets": [
                    {
                        "data": data,
                        "backgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                        ],
                        "hoverBackgroundColor": [
                            "#FF6384",
                            "#36A2EB",
                        ]
                    }]
            }
    return data_dict
