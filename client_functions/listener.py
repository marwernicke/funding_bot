# my files
from Strategies import manager

async def all(notification, user):
    if type(notification) == list:

        if notification[1] == 'foc': #funding offer closed
            offer_id = notification[2][0]
            print('_#_ ORDER CLOSED {}'.format(user.offers[offer_id]))
            if offer_id in user.offers:
                del user.offers[offer_id]


        if notification[1] == 'fon': #funding offer notification (new order place)
            offer_id = notification[2][0]
            fcoin = notification[2][1]
            creation_date = notification[2][3]
            amount = notification[2][5]
            rate = notification[2][14]
            per = notification[2][15]
            user.offers[offer_id] =  {'offer_id': offer_id, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per}
            print('_#_ NEW ORDER PLACED {}'.format(user.offers[offer_id]))

        if notification[1] == 'fte': #funding trade executed
            print('TRADEEEEE', notification)
            offer_id = notification[2][0]
            print('_#_ FUNDING TRADE EXECUTED {}'.format(user.offers[offer_id]))
            if offer_id in user.offers:
                del user.offers[offer_id]

        if notification[1] == 'fcc': #funding credit closed
            credit_id = notification[2][0]
            if credit_id in user.credits:
                del user.credits[credit_id]
            ##### VA A DONDE SE CONVIERTE ????????

        if notification[1] == 'fcn': #funding credit new
            credit_id = notification[2][0]
            fcoin = notification[2][1]
            creation_date = notification[2][3]
            amount = notification[2][5]
            rate = notification[2][11]
            per = notification[2][12]
            user.credits[credit_id] =  {'credit_id':credit_id, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per}
            print('_#_ FUNDING CREDIT NEW {}'.format(user.credits[credit_id]))
            ##### VA DE DONDE SE CONVIERTE ????????

        if notification[1] == 'wu': #wallet update
            format = notification[2][0]
            coin = notification[2][1]
            balance =  notification[2][2]
            available = notification[2][4]
            user.wallets[coin] = {'format':format, 'balance':balance, 'available':available }
            if (format == "funding") & (available > 50):
                await manager.balance_available(user,coin, available)
