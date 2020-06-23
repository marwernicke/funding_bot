# my files
from Strategies import manager
import time

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
                #### CHEHCO #### UPDATE ORDER TO DATA BASE
                del user.offers[offer_id]

        if notification[1] == 'fon': #funding offer notification (new order place)
            user_id = user.id
            offer_id = notification[2][0]
            fcoin = notification[2][1]
            creation_date = notification[2][3]
            amount = notification[2][5]
            rate = notification[2][14]
            per = notification[2][15]
            user.offers[offer_id] =  {'user_id': user_id, 'offer_id': offer_id, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per,'closed_date': 0, 'was_executed':0 }
            print('_#_ NEW ORDER PLACED {}'.format(user.offers[offer_id]))
            #### CHEHCO #### NEW ORDER TO DATA BASE

        if notification[1] == 'fcc': #funding credit closed
            user_id = user.id
            credit_id = notification[2][0]
            start_date = notification[2][3]
            end_date = notification[2][4]
            rate = notification[2][11]
            earn_money = (end_date - start_date) * (rate / 24* 60* 60 * 1000) * 0.85
            piad_fees = earn_money/0.85*0.15
            if credit_id in user.credits:
                user.credits[credit_id]['end_date'] = end_date
                user.credits[credit_id]['earn_money'] = earn_money
                user.credits[credit_id]['piad_fees'] = piad_fees
                #### CHEHCO #### UPDATE CREDIT TO DATA BASE
                del user.credits[credit_id]

        if notification[1] == 'fcn': #funding credit new
            user_id = user.id
            credit_id = notification[2][0]
            fcoin = notification[2][1]
            creation_date = notification[2][3]
            amount = notification[2][5]
            rate = notification[2][11]
            per = notification[2][12]
            user.credits[credit_id] =  {'user_id': user_id, 'credit_id':credit_id, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per, 'end_date':0, 'earn_money':0, 'piad_fees':0}
            print('_#_ FUNDING CREDIT NEW {}'.format(user.credits[credit_id]))
            #### CHEHCO #### NEW CREDIT TO DATA BASE

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
            print('_#_ {} WALLET UPDATE {}'.format(coin, user.wallets[coin]))
            #### CHEHCO #### WALLET TO DATA BASE
            if (coin in user.coins) & (format == "funding") & (available > 50):
                await manager.balance_available(user,coin, available)
