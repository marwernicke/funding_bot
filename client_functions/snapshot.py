def snapshot(coins,user):

    @user.bfx.ws.on('funding_offer_snapshot')
    def log_offers(offers):
        user.offers = {}
        for offer in offers[2]:
            id_offer = offer[0]
            fcoin = offer[1]
            creation_date = offer[3]
            amount = offer[5]
            rate = offer[14]
            per = offer[15]
            user.offers[id_offer] =  {'id_offer': id_offer, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per}

    @user.bfx.ws.on('funding_credit_snapshot')
    def log_credits(credits):
        user.credits = {}
        for credit in credits:
            id_credit = credit[0]
            fcoin = credit[1]
            creation_date = credit[3]
            amount = credit[5]
            rate = credit[11]
            per = credit[12]
            user.credits[id_credit] =  {'id_credit':id_credit, 'coin':fcoin, 'creation_date': creation_date, 'amount':amount, 'rate':rate, 'per': per}
