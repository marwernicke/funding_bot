import asyncio
from datetime import datetime as dt
import time
#### my Files
from user import user
from keys import TEST_API_KEY, TEST_API_SECRET, API_KEY, API_SECRET
from client_functions import listener

def horly_cancel(user):
    while True:
        time.sleep(10)# an hour
        actual_time = dt.now()
        print('### check_cancel_all_offers() called at {}'.format(actual_time))
        asyncio.run(user.cancel_all_offers())

def run(user):
    @user.bfx.ws.on('all')
    async def log_updates(data):
        #print('____',data)
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
        print(user.wallets[wallet])
    print("##################################################")

    #horly_cancel(user)


#test = user('Test_758',TEST_API_KEY, TEST_API_SECRET,'usd')
#run(test)

marcos = user('Mars_859',API_KEY,API_SECRET,['usd'])

run(marcos)
