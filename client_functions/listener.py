#Needed packages
import time
#pip install pymongo & pip install pymongo[srv] needed for web clusters.
import pymongo

# my files
from Strategies import manager

async def all(notification, user):
    if type(notification) == list:

        if notification[1] == 'foc': #funding offer closed
            user_id = user.id
            offer_id = notification[2][0]
            closed_date = notification[2][3]
            status = notification[2][10]
            if status == 'CANCELED':
                was_executed = 0
            else:
                first_word_of_status = status.split(' ', 1)[0] # status example : 'EXECUTED at 0.0253% (50.0)'
                if first_word_of_status == 'EXECUTED':
                    was_executed = 1
            if offer_id in user.offers:
                user.offers[offer_id]['closed_date'] = closed_date
                user.offers[offer_id]['was_executed'] = was_executed
                print('_#_ ORDER CANCELED {}'.format(user.offers[offer_id]))
                #Connection to data base, order document updated in 'orders' collection.
                user.mongo_user.change_offer_status(offer_id = offer_id,
                                                    closed_date = closed_date,
                                                    was_executed = was_executed)
                del user.offers[offer_id]

        if notification[1] == 'fon': #funding offer new (new order place)
            user_id = user.id
            offer_id = notification[2][0]
            fcoin = notification[2][1]
            creation_date = notification[2][3]
            amount = notification[2][5]
            rate = notification[2][14]
            per = notification[2][15]
            user.offers[offer_id] =  {'user_id': user_id, 'offer_id': offer_id, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per,'closed_date': 0, 'was_executed':0 }
            print('_#_ NEW ORDER PLACED {}'.format(user.offers[offer_id]))
            #Connection to data base, new order document in 'orders' collection.
            user.mongo_user.new_offer(user.offers[offer_id])

        if notification[1] == 'fcc': #funding credit closed
            user_id = user.id
            credit_id = notification[2][0]
            start_date = notification[2][13]
            end_date = notification[2][14]
            rate = notification[2][11]
            earn_money = (end_date - start_date) * (rate / 24* 60* 60 * 1000) * 0.85
            piad_fees = earn_money/0.85*0.15
            if credit_id in user.credits:
                user.credits[credit_id]['end_date'] = end_date
                user.credits[credit_id]['earn_money'] = earn_money
                user.credits[credit_id]['piad_fees'] = piad_fees
                #Connection to data base, credit document updated in 'credits' collection.
                "Is better instead of updating to create a new document?"
                user.mongo_user.change_offer_status(credit_id = credit_id,
                                                    end_date = end_date,
                                                    earn_money = earn_money,
                                                    paid_fees = paid_fees)
                del user.credits[credit_id]

        if notification[1] == 'fcn': #funding credit new
            user_id = user.id
            credit_id = notification[2][0]
            fcoin = notification[2][1]
            creation_date = notification[2][13]
            amount = notification[2][5]
            rate = notification[2][11]
            per = notification[2][12]
            user.credits[credit_id] =  {'user_id': user_id, 'credit_id':credit_id, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per, 'end_date':0, 'earn_money':0, 'piad_fees':0}
            print('_#_ FUNDING CREDIT NEW {}'.format(user.credits[credit_id]))
            #Connection to data base, new credit document in 'credits' collection.
            user.mongo_user.new_credit(user.offers[credit_id])

        if notification[1] == 'wu': #wallet update
            user_id = user.id
            timestamp = time.time()
            format = notification[2][0]
            coin = notification[2][1]
            balance =  notification[2][2]
            available = notification[2][4]
            rate_curr_usd = 1
            if coin in user.wallets:
                user.wallets[coin][format] = {'balance':balance, 'available':available }
            else: #if coin not in users wallets the coin is added to the wallets
                user.wallets[coin] = {format : {} }
                user.wallets[coin][format] = {'balance':balance, 'available':available }
                #Conection to data base. Coin added to data base users document.
                user.mongo_user.update_one(coin = coin)
            print('_#_ {} WALLET UPDATE {}'.format(coin, user.wallets[coin]))
            #Connection to data base, new wallet snapshot in 'walletSnapshots' collection.
            new_wu_data = {
                           'timestamp': time.time()*1000,
                           'currency': coin,
                           'balance': balance,
                           'available': available,
                           'rate_curr_usd': 1,
                           'format': format
                            }
            user.mongo_user.new_wallet_snapshot(doc_data = new_wu_data)
            if (coin in user.coins) & (format == "funding") & (available > 50):
                await manager.balance_available(user,coin, available)
