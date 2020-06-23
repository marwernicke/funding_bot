#Document information
document_data = {
                 'author': 'checho651',
                 'name': 'conection_test.py',
                 'description': 'Short sctipt to test mongo_db_conection',
                 'version': '2.0.0'
                 }


#Needed packages
import pandas as pd
import pymongo
import time

#Own files
import mongo_db_conection as mdbc


#Creates a pymongo.MongoClient in order to get access to de databases available.
mongo_user = 'FundingBot'
mongo_password = 'Funding3575'
mongo_client = mdbc.mongo_db_conection(mongo_user, mongo_password, mg_user_info = True)

# #Creates an instance of the class 'Bot_user'
maw = mdbc.Bot_user(client = mongo_client, user_uid = 35353535)

# new_user_data = {
#                 'name': 'marcos',
#                 'surname': 'wernicke',
#                 'user_name': 'maw',
#                 'uid': 35353535,
#                 'API_key': 'unknow',
#                 'API_secret': 'unknow',
#                 'coins': [],
#                 'timestamp': time.time()*1000,
#                 'is_active': 0,
#                 'start_amount': 0,
#                 'earnings': 0,
#                 'current_amount': 0
#                 }
# mdbc.new_bot_user(client = mongo_client, user_data = new_user_data)

# new_wallet_snapshot = {
#                        'uid': 0,
#                        'timestamp': time.time()*1000,
#                        'currency': 'usd',
#                        'amount': 1000,
#                        'available': 100,
#                        'rate_curr_usd': 1
#                        }


new_offer_data = {
                  'uid': 0,
                  'id_offer': 100000,
                  'creation_date': time.time()*1000,
                  'coin': 'usd',
                  'amount': 1000,
                  'per': 30,
                  'rate': 0.003,
                  'closed_date': 0,
                  'was_executed': 0,
                  }

new_credit_data = {
                    'uid': 0,       
                    'id_credit': 10,
                    'start_date': time.time()*1000,
                    'coin': 'usd',
                    'amount': 500,
                    'per': 30,
                    'rate': 0.003,
                    'from_offer': 125626,
                    'end_date': 0,
                    'earn_money': 15,   
                    'paid_fees': 3   
                    }

# #Aggregate query.
# #Matches 'was_executed': 0, creates a group '_id' : '$coin', gives the 'total'.


# #Receive a list of dictionaries with each sum.
# total_list = list(ezm.col_offers.aggregate(agg_query))