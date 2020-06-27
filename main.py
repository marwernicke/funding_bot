#Needed packages
import asyncio
from datetime import datetime as dt
import time
import sched
import asyncio
#pip install pymongo & pip install pymongo[srv] needed for use of web clusters.
import pymongo

#### my Files
from user import user
from keys import TEST_API_KEY, TEST_API_SECRET, API_KEY, API_SECRET, mongo_user, mongo_password
from client_functions import listener, orders
from mongodb import mongo_db_conection as mdbc

def print_user_data(user):
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

def horly_cancel(loop):
    actual_time = dt.now()
    print('### cancel_all_offers() called at {}'.format(actual_time))
    for user in users:
        print_user_data(user)
        asyncio.run(orders.cancel_all_offers(user))
    loop.enter(3600, 1, horly_cancel, (loop,))

def run(user):
    @user.bfx.ws.on('all')
    async def on_all(data):
        await listener.all(data,user)
    time.sleep(5) # time to load
    print_user_data(user)

########### Running starts here ###########
#Creates a pymongo.MongoClient in order to get access to de databases available.
#The connection is with a web cluster. All users connect to same MongoClient.
mg_user = mongo_user
mg_password = mongo_password
mongo_client = mdbc.mongo_db_conection(mg_user, mg_password, mg_user_info = True)

test = user('Test_758', TEST_API_KEY, TEST_API_SECRET, ['USD'],
            uid = 36363636, mongo_client = mongo_client)
marcos = user('Mars_859', API_KEY, API_SECRET, ['USD'],
            uid = 35353535, mongo_client = mongo_client)users = [marcos,test]
            
for user in users:
    run(user)

# runs loop for hourly cancel
loop = sched.scheduler(time.time, time.sleep)
loop.enter(60, 1, horly_cancel, (loop,))
loop.run()

