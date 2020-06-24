from datetime import datetime as dt
import time
import sched
import asyncio
#### my Files
from user import user
from client_functions import orders
from keys import TEST_API_KEY, TEST_API_SECRET, API_KEY, API_SECRET
from client_functions import listener

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
    loop.enter(60, 1, horly_cancel, (loop,))

def run(user):
    @user.bfx.ws.on('all')
    async def on_all(data):
        await listener.all(data,user)
    time.sleep(5) # time to load
    print_user_data(user)

########### Running starts here ###########
test = user('Test_758',TEST_API_KEY, TEST_API_SECRET,['USD'])
marcos = user('Mars_859',API_KEY,API_SECRET,['USD'])
users = [marcos,test]
for user in users:
    run(user)

# runs loop for hourly cancel
loop = sched.scheduler(time.time, time.sleep)
loop.enter(60, 1, horly_cancel, (loop,))
loop.run()
