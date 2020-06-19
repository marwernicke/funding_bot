document_data = {
                 'author': 'checho651',
                 'name': 'conection_test.py',
                 'description': 'Short sctipt to test mongo_db_conection',
                 'version': '1.0.0'
                 }

import pandas as pd
import pymongo
from datetime import datetime, timedelta
import mongo_db_conection as mdbc


#Creates a pymongo.MongoClient in order to get access to de databases available.
mongo_user = 'FundingBot'
mongo_password = 'Funding3575'
mongo_client = mdbc.mongo_db_conection(mongo_user, mongo_password, mg_user_info = True)

#Creates an instance of the class 'Bot_user'
ezm = mdbc.Bot_user(client = mongo_client, user_dni = 35381137)

new_user_data = {
                'name': 'marcos',
                'surname': 'wernicke',
                'dni': 35353535,
                'API_key': 'unknow',
                'API_secret': 'unknow',
                'start_date': datetime.now(),
                'start_amount': 0,
                'is_active': 0,
                'earnings': 0,
                'current_amount': 0
                }

new_offer_data = {
                  'id_offer': 100000,
                  'creation_date': datetime(year = 2020, month = 6, day = 14,
                                            hour = 15, minute = 5, second = 15),
                  'coin': 'usd',
                  'amount': 1000,
                  'per': 30,
                  'rate': 0.003,
                  'closed_date': 0,
                  'was_executed': 0,
                  }

new_credit_data = {
                   'id_credit': 10,
                   'start_date': datetime.now(),
                   'coin': 'usd',
                   'amount': 500,
                   'per': 30,
                   'rate': 0.003,
                   'from_offer': 125626,
                   'end_date': 0,
                    }
