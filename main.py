#Document information
document_data = {
                 'author': 'marwernicke',
                 'name': 'main.py',
                 'description': 'Main script, runs the funding bot',
                 'version': '1.0.0',
                 'new_update': 'checho651 conection to monogodb'
                 }

#Needed packages
import asyncio
from datetime import datetime as dt
import time
#pip install pymongo & pip install pymongo[srv] needed for use of web clusters.
import pymongo

#### my Files
from user import user
from keys import TEST_API_KEY, TEST_API_SECRET, API_KEY, API_SECRET, mongo_user, mongo_password
from client_functions import listener
from mongodb import mongo_db_conection as mdbc
"""
def horly_cancel(user):
    while True:
        time.sleep(3600)# an hour
        print("####################### {} ###########################".format(user.user_name))
        print("____CREDITS")
        for credit in user.credits:
            print(user.credits[credit])
        print("____OFFERS")
        for offer in user.offers:
            print(user.offers[offer])
        print("____WALLETS")
        for wallet in user.wallets:
            print(user.wallets[wallet])
        print("##################################################")
        actual_time = dt.now()
        print('### check_cancel_all_offers() called at {}'.format(actual_time))
        asyncio.run(user.cancel_all_offers())

def run(user):
    @user.bfx.ws.on('all')
    async def on_all(data):
        await listener.all(data,user)

    time.sleep(2)

    print("####################### {} ###########################".format(user.user_name))
    print("____CREDITS")
    for credit in user.credits:
        print(user.credits[credit])
    print("____OFFERS")
    for offer in user.offers:
        print(user.offers[offer])
    print("____WALLETS")
    for wallet in user.wallets:
        print(wallet,user.wallets[wallet])
    print("##################################################")

    #horly_cancel(user)

#Creates a pymongo.MongoClient in order to get access to de databases available.
#The connection is with a web cluster. All users connect to same MongoClient.
mg_user = mongo_user
mg_password = mongo_password
mongo_client = mdbc.mongo_db_conection(mg_user, mg_password, mg_user_info = True)

test = user('Test_758', TEST_API_KEY, TEST_API_SECRET, ['USD'],
            uid = 36363636, mongo_client = mongo_client)
run(test)

marcos = user('Mars_859', API_KEY, API_SECRET, ['USD'],
              uid = 36363636, mongo_client = mongo_client)
run(marcos)
