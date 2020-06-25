def snapshot(coins,user):

    @user.bfx.ws.on('funding_offer_snapshot')
    def log_offers(offers):
        user.offers = {}
        user_id = user.user_name
        for offer in offers[2]:
            offer_id = offer[0]
            coin = offer[1]
            creation_date = offer[3]
            amount = offer[5]
            rate = offer[14]
            per = offer[15]
            user.offers[offer_id] =  {'user_id': user_id, 'offer_id': offer_id, 'creation_date': creation_date, 'coin':coin, 'amount':amount, 'rate':rate, 'per': per, 'closed_date': 0, 'was_executed':0}

    @user.bfx.ws.on('funding_credit_snapshot')
    def log_credits(credits):
        user.credits = {}
        user_id = user.user_name
        #List of credits is in index 2?
        for credit in credits[2]:
            credit_id = credit[0]
            coin = credit[1]
            creation_date = credit[3]
            amount = credit[5]
            rate = credit[11]
            per = credit[12]
            user.credits[credit_id] =  {'user_id': user_id, 'credit_id':credit_id, 'creation_date': creation_date, 'coin':coin, 'amount':amount, 'rate':rate, 'per': per, 'end_date':0, 'earn_money':0, 'piad_fees':0 }
