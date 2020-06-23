import time

# my files
from connection import conect
from client_functions import orders
from client_functions import snapshot

class user():
    def __init__(self, user_name, API_KEY,  API_SECRET, coins):
        self.user_name = user_name
        self.id = user_name
        self.bfx = conect(API_KEY, API_SECRET)
        self.coins = coins
        self.wallets = {}
        snapshot.snapshot(coins, self)

        #run user bot
        self.bfx.ws.run()

    async def cancel_all_offers(self):
        await orders.cancel_all_offers(self)
        print(self.offers)
