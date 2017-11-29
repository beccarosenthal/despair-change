from datetime import datetime

from collections import defaultdict
from flask import Flask, redirect, request, session, jsonify
from sqlalchemy import func, extract, Date, cast, DATE

from model import (User, Organization, Transaction,
                   UserOrg, State, Referral,
                   connect_to_db, db)

BACKGROUND_COLORS = ["#C72DB3", "#D9A622", "#2CA248", "#6574DA",
                     "#C72D2D", "#2DC7C0", "#FF6384", "#FEFF29", ]
HOVER_BACKGROUND_COLORS = ["#2DC7C0", "#FF6384", "#FEFF29","#000000",
                           "#36A2EB", "#FF00FF", "#6574DA", "#C72D2D", ]


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
    # print "ids of referred users: ", referred_user_ids

    user_data = [] #dictionaries with donor_category: amount pairs (my donations, donation footprint, etc)   user_data = [] #amount of money user gave per org in order of orgs
    footprint_data = [] #amount of money footprint gave per org in order of orgs
    org_names = [] #name of org

    # print org_names
    for org in orgs:
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
    # print
    # print "data dict before"
    # print data_dict

    if referred_user_ids:
        data_dict["datasets"] += footprint_dataset

    ##TODO figure out how to make sure that no footprint data shows up if know footprint
    # if footprint_data:
    #     data_dict['datasets'].append({   "label": ["My Footprint"],
    #                     "data": footprint_data,
    #                     "backgroundColor": HOVER_BACKGROUND_COLORS[0],
    #                     "hoverBackgroundColor": BACKGROUND_COLORS[1]
    #                 },)

    # print "footprint data"
    # print footprint_data
    # print
    # print "data_dict after"
    # print
    # print data_dict

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

def json_org_donations_datetime():
    """generate data for line chart of donations over time"""
    # # queries tuple of($sum, date, org_id, #donations to that org on that date)
    group_param = cast(Transaction.timestamp, DATE)
    transactions = (db.session.query(func.sum(Transaction.amount),
                                     group_param,
                                     Transaction.org_id,
                                     func.count(Transaction.transaction_id))
                              .group_by(group_param,
                                        Transaction.org_id)
                              .order_by(group_param,
                                        Transaction.org_id)
                              .all())

    # org_ids = [org.org_id for org in Organization.query.all()]
    orgs = Organization.query.all()

    #make dictionary with dates as keys
    data_by_date = {}
    for item in transactions:
        data_by_date[item[1]] = {}
    #at each date, make orgs keys with
    for key in data_by_date.keys():
        for org in orgs:
            data_by_date[key][org.name] = {"total_donated": None,
                                           "num_donations": None,
                                           "display_name": org.short_name}

    #populate the dictionary with info specific to each org
    for org in orgs:
        transactions = Transaction.get_transactions_by_org_date(org.org_id)

        for transaction in transactions:
            total_donated, num_donations, date  = transaction
            data_by_date[date][org.name]['total_donated'] = total_donated
            data_by_date[date][org.name]['num_donations'] = num_donations


    datetime = []
    label_dates = []
    org_data = []


    print "data_by_date.items()"
    print data_by_date.items()
    # for i in range(len(data_by_date.keys())):
    for date, org_dict in  data_by_date.items():
        print date
        print org_dict
        print
        datetime.append(date)
        org_data.append(org_dict)

    for date in datetime:
        label_dates.append(date.strftime("%m/%d/%y"))

    data_dict = {
                "labels": label_dates,
                # "datasets": generate_datasets(org_data, "num_donations"),
                "datasets":  generate_datasets(org_data, "total_donated")
            }
    ###AT THIS POINT, WE NEED DATA BY ORG LIST THAT UNPACKS THE ORG DATA LIS


    ###FOR NOW I"M JUST DOING TOTAL $, not num_donations. The nums are there

    return jsonify(data_dict)

def generate_datasets(org_data_dict, data_key):
    """given items date dict, assembles dataset"""

    orgs = Organization.query.all()
    datasets = []
    count = 0
    for org in orgs:
        num_donations = []
        total_donated = []
        backgroundColor = BACKGROUND_COLORS[count]
        hoverBackgroundColor = HOVER_BACKGROUND_COLORS[count]
        for item in org_data_dict:

            label = org.short_name
            ##Account for null data points
            if item[org.name]['num_donations']:
                num_donations.append(item[org.name]['num_donations'])
            else:
                num_donations.append(0)
            if item[org.name]['total_donated']:
                total_donated.append(item[org.name]['total_donated'])
            else:
                total_donated.append(0)

        if data_key == "num_donations":
            data = num_donations
        else:
            data = total_donated
        data_dict = {  "label": [label],
                        "data": data,
                        "backgroundColor": backgroundColor,
                        "hoverBackgroundColor": hoverBackgroundColor,
                    },

        # import pdb; pdb.set_trace()
        datasets += data_dict
        # print data_dict
        count += 1
    return datasets


def json_total_donations_line():
    """generate data for line chart of donations over time"""

    #queries for tuple of ($sum, #donations, date)
    group_param = cast(Transaction.timestamp, DATE) #can change group param to group query by different things
    transactions = (db.session.query(func.sum(Transaction.amount),
                                     func.count(Transaction.amount),
                                     # func.count(Transaction.user_id),
                                     group_param)
                              .group_by(group_param)
                              .order_by(group_param)
                              .all())

    # # queries tuple of($sum, date, org_id, #donations to that org on that date)
    # transactions = (db.session.query(func.sum(Transaction.amount),
    #                                  group_param,
    #                                  Transaction.org_id,
    #                                  func.count(Transaction.transaction_id))
    #                           .group_by(group_param,
    #                                     Transaction.org_id)
    #                           .order_by(group_param,
    #                                     Transaction.org_id)
    #                           .all())

    count = []
    total = []
    # num_donors = []
    dates = []
    label_dates = []

    for data in transactions:
        total.append(data[0])
        count.append(data[1])
        # num_donors.append(data[2])
        dates.append(data[2])

    #make dates presentable
    for date in dates:
        label_dates.append(date.strftime("%m/%d/%y"))

    print transactions
    # import pdb; pdb.set_trace()


    data_dict = {
                "labels": label_dates,
                "datasets": [
                    {   "label": "Number of Donations",
                        "data": count,
                        "fill": False,
                        "borderColor": BACKGROUND_COLORS[1],
                        "pointBorderColor": BACKGROUND_COLORS[0],
                        "strokeColor": HOVER_BACKGROUND_COLORS[0],
                        "pointHoverBackgroundColor": "yellow",
                        "lineTension": 0
                                            },

                    {   "label": "Amount Donated",
                        "data": total,
                        "fill": False,
                        "borderColor": BACKGROUND_COLORS[2],
                        "pointBorderColor": BACKGROUND_COLORS[3],
                        "strokeColor": HOVER_BACKGROUND_COLORS[4],
                        "pointHoverBackgroundColor": "blue",
                        "lineTension": 0
                                            },

                    # {  "label": "Number of Donors",
                    #     "data": num_donors,
                    #     "fill": False,
                    #     "borderColor": BACKGROUND_COLORS[4],
                    #     "pointBorderColor": BACKGROUND_COLORS[5],
                    #     "strokeColor": HOVER_BACKGROUND_COLORS[6],
                    #     "pointHoverBackgroundColor": "red",
                    #     "lineTension": 0
                    #                         },
                                            ]
            }

    # data_dict['datasets'].extend([amount_data, donor_data])
    print "figure out data_dict[datasets]"
    # import pdb; pdb.set_trace()
    return jsonify(data_dict)



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
