import time

# my files
from connection import conect
from client_functions import orders
from Strategies import rolling_high


class user():
    def __init__(self,API_KEY, API_SECRET):
        self.bfx = conect(API_KEY, API_SECRET)
        #self.wallet = read_wallet()
        #self.offers = read_offers()
        #self.credits = read_credits()
        #self.unconfirmed_credits = {} ???

        #run user bot
        self.bfx.ws.run()

    async def new_offer(self, coin, ammount):
        rate, per = await rolling_high.strategy(coin)
        offer_id = await orders.create_funding(amount, per, rate, coin, self.bfx)
        if offer_id != None:
            pass #save_offer()

    async def cancel_offer(self, coin, ammount):
        



marcos = user('QvjlxWMsJi7Sf1mD335qecVTDQBHeZBiVYxiqLsdYKg','xErtLXpzPWktAPbkwJeJL7wdP2bNkWm50ezfGqll6Ck')
@marcos.bfx.ws.on('all')
def log_updates(data):
    #listener.all(data)
    print('---------')
