import time
import pymongo


# my files
from connection import conect
from client_functions import orders
from client_functions import snapshot
from mongodb import mongo_db_conection as mdbc



class user():
    def __init__(self, user_name, API_KEY,  API_SECRET, coins, uid: int, mongo_client: pymongo.MongoClient):
        self.user_name = user_name
        self.id = user_name
        self.bfx = conect(API_KEY, API_SECRET)
        self.coins = coins
        self.wallets = {}
        snapshot.snapshot(coins, self)

        #run user bot
        self.bfx.ws.run()

        #Creates an instance of the class 'Bot_user' to conect to mongo database
        self.mongo_user = mdbc.Bot_user(client = mongo_client, user_uid = uid)

    async def cancel_all_offers(self):
        await orders.cancel_all_offers(self)
        print(self.offers)
