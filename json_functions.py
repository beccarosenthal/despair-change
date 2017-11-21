from collections import defaultdict
from flask import Flask, redirect, request, session, jsonify
from sqlalchemy import func

from model import (User, Organization, Transaction,
                   UserOrg, State, Referral,
                   connect_to_db, db)

BACKGROUND_COLORS = ["#C72DB3", "#D9A622", "#2CA248", "#6574DA",
                     "#C72D2D", "#2DC7C0", "#FF6384", "#FEFF29", ]
HOVER_BACKGROUND_COLORS = ["#2DC7C0", "#FF6384", "#FEFF29","#000000",
                           "#36A2EB", "#FF00FF", "#6574DA", "#C72D2D",  ]


################################################################################

# pseudocode of what i want with user-impact-bar
# labels: [orgs]
# datasets
#     label: my donations
#         org name: $amount I donated to each org
#     my impact
#         org name: $ amount [my referred users] donated to each org
#     total donations
#         org name $ amount all users donated to each org

# labels[labels]
# user:

################################################################################

def json_stacked_user_impact_bar(user_object):
    """returns json data for chart with user donations and donations
    generated by users referred by that user"""

    #get list of orgs
    #TODO figure out how to make list of orgs only org user has donated to
    orgs = Organization.query.all()


    #list of all users referred by me
    referred_by_user = get_all_referred_by_user(user_object)

    #get list of user_ids to make querying for sum of donations easier
    referred_user_ids = [user.user_id for user in referred_by_user]
    print "ids of referred users: ", referred_user_ids

    user_data = [] #dictionaries with donor_category: amount pairs (my donations, donation footprint, etc)   user_data = [] #amount of money user gave per org in order of orgs
    footprint_data = [] #amount of money footprint gave per org in order of orgs
    org_names = [] #name of org
    print "*********ORG NAMES************"
    print org_names
    for org in orgs:
        print "current org in loop:", org
        print "*********ORG NAMES************"
        print org_names
        #query for sum of my donations to each org

        my_donations = (db.session.query(func.sum(Transaction.amount))
            .filter(Transaction.org_id == org.org_id,
                Transaction.status == "pending delivery to org",
                Transaction.user_id == user_object.user_id)
            .all())[0][0]
        if referred_user_ids:
            donation_footprint = (db.session.query(func.sum(Transaction.amount))
                .filter(Transaction.org_id == org.org_id,
                    Transaction.status == "pending delivery to org",
                    Transaction.user_id.in_(referred_user_ids))
                .all())[0][0]
        else:
            donation_footprint = 0
        # total_donations = (db.session.query(func.sum(Transaction.amount))
        #     .filter(Transaction.org_id == org.org_id,
        #         Transaction.status == "pending delivery to org")
        #     .all())

        #add org and data to the lists going into the datasets only if there's data
        if my_donations > 0 or donation_footprint > 0:
            user_data.append(my_donations)
            footprint_data.append(donation_footprint)
            org_names.append(org.name[:20])
        print "my donations:", my_donations
        print "my footprint data", footprint_data
        #TODO figure out why this errors out
        # donations[org.name]['Additional Donations'] = total_donations - my_donations - donation_footprint

    data = []
    datasets = []

    data_dict = {
                "labels": org_names,
                "datasets": [
                    {   "label": ["My Donations"],
                        "data": user_data,
                        "backgroundColor": BACKGROUND_COLORS[0],
                        "hoverBackgroundColor": HOVER_BACKGROUND_COLORS[1]
                    },
                    ]
            }

    #If person has a footprint, append it to the data_dict
    footprint_dataset = {"label": ["My Footprint"],
                        "data": footprint_data,
                        "backgroundColor": HOVER_BACKGROUND_COLORS[0],
                        "hoverBackgroundColor": BACKGROUND_COLORS[1]
                    },
    print
    print "data dict before"
    print data_dict


    if referred_user_ids:
        data_dict["datasets"] += footprint_dataset

    ##TODO figure out how to make sure that no footprint data shows up if know footprint
    # if footprint_data:
    #     data_dict['datasets'].append({   "label": ["My Footprint"],
    #                     "data": footprint_data,
    #                     "backgroundColor": HOVER_BACKGROUND_COLORS[0],
    #                     "hoverBackgroundColor": BACKGROUND_COLORS[1]
    #                 },)

    print "footprint data"
    print footprint_data
    print
    print "data_dict after"
    print
    print data_dict

    return jsonify(data_dict)


def json_user_impact_bar(user_object):
    """returns json data for chart with user donations by org"""

    current_user_id = user_object.user_id

    #Create dictionary with key value pairs of {org_id: amt donated by user}
    donations_by_org = {}
    for transaction in user_object.transactions:
        if transaction.status == "pending delivery to org":
            org_name = Organization.query.get(transaction.org_id).name
            donations_by_org[org_name] = (donations_by_org.get(org_name, 0) +
                                          transaction.amount)

    orgs = [] #name of org
    data = [] #amount of money

    for org, amount in donations_by_org.items():
        orgs.append(org[:30])
        data.append(amount)

    data_dict = {
                "labels": orgs,
                "datasets": [
                    {   "label": "My Donations",
                        "data": data,
                        "backgroundColor": BACKGROUND_COLORS,
                        "hoverBackgroundColor": HOVER_BACKGROUND_COLORS
                    }]
            }

    return jsonify(data_dict)


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
                    {   "label": ["Our Impact"],
                        "data": data,
                        "backgroundColor": BACKGROUND_COLORS,
                        "hoverBackgroundColor": HOVER_BACKGROUND_COLORS
                    }]
            }

    return jsonify(data_dict)

##TODO separate out query helper functions into its own file
#############QUERY HELPER FUNCTION########

def get_all_referred_by_user(user_object):
    """given user_object, returns list of users in referred chain from primary user

    #HYPOTHETICAL EXAMPLE:
    #User1 referred User2 and User3. User3 referred User4.

    >>>get_all_referred_by_user(User1)
        >>>[User2, User3, User4]
        """

    ##recursive function
    chain = []
    for user in user_object.referred:
        chain += [user] + get_all_referred_by_user(user)
    return chain
