#Document information
document_data = {
                 'author': 'checho651',
                 'name': 'mongo_db_conection.py',
                 'description': '''Creates a mongo conection class with Methods
                                    to update data easily to each Bot_user''',
                 'version': '2.0.1',
                 'new_update': 'modify variable names, credit update options.'
                 }

#Needed packages
import pymongo

class Bot_user:
    """
    Before creating an instance of the class, user need to be registered in
    proyect "FundingBot", database "funding_bfx", collection 'users' as
    a document.
    If client is not registered it returns None.
    """
    def __init__(self, client: pymongo.MongoClient, user_uid: int):
        """
        Gets the data of the user from 'users' collection.
        """
        self.client = client
        self.user_uid = user_uid
        #Checks if conection was successful, gets client data form users_data
        try:
            #Collection where user data is stored.
            self.col_data = self.client.funding_bfx.users
            self.user_data = self.col_data.find_one({'uid': self.user_uid})

            #User attributes
            self._id = self.user_data['_id']
            self.name = self.user_data['name']
            self.surname = self.user_data['surname']
            self.user_name = self.user_data['user_name']
            self.uid = self.user_data['uid']
            self.API_key = self.user_data['API_key']
            self.API_secret = self.user_data['API_secret']
            self.timestamp = self.user_data['timestamp']
            self.start_amount = self.user_data['start_amount']

            #Database and collections name where historical data is stored.
            self.db_records = self.client.funding_bfx
            self.col_wallets = self.db_records['walletSnapshots']
            self.col_offers = self.db_records['offers']
            self.col_credits = self.db_records['credits']

        except:
            print('User :',self.user_uid, 'not found')

    ##Methods associated with the class
    def update (self):
        """
        Method to update modified values from database by other functions.
        """
        self.__init__(self.client, self.user_uid)

    #Status info methods.
    def is_active(self):
        try:
            return self.col_data.find_one({'uid': self.user_uid})['is_active']
        except:
            print('Conection with database failed')

    def coins(self):
        try:
            return self.col_data.find_one({'uid': self.user_uid})['coins']
        except:
            print('Conection with database failed')

    def earnings(self):
        try:
            agg_query = [{'$match': {'uid': self.uid}},
             {'$group': {'_id': '$coin', 'total': {'$sum': '$earnings'}}}]
            #Receive a list of dictionaries with each sum.
            total_list = list(self.col_offers.aggregate(agg_query))
            return total_list
        except:
            print('Conection with database failed')

    def current_amount(self):
        try:
            return self.col_data.find_one({'uid': self.user_uid})['current_amount']
        except:
            print('Conection with database failed')

    def update_one(self, coin = '', **kwargs):
        """
        Parameters
        ----------
        coin : str
            Currency symbol. Only accepts one value as string.
        **kwargs : TYPE
            Can update any value from users document.

        Updates values from users document.

        Returns
        -------
        None.
        """
        try:
            for key, value in kwargs.items():
                self.col_data.update_one({'uid': self.uid},
                            {"$set":
                                {key: value}
                            }
                                   )
            if coin:
                if coin in self.coins():
                    print(f'Coin {coin} already exists')
                else:
                    self.col_data.update_one({'uid': self.uid},
                                                {"$push":
                                                    {'coins': coin}
                                                }
                                             )
        except:
            print('Update could not be performed')

    #Wallet methods.
    def wallet_info (self):
        "Returns a dictionary with las walletSnapshot for each coin in user coins"
        wallet_dict = dict()
        try:
            for coin in self.coins():
                last_update = self.col_wallets.find_one({'uid': self.uid, 'currency': coin},
                                                        sort = [('timestamp', -1)])
                if last_update:
                    wallet_dict[coin] = {'balance': last_update['balance'],
                                           'available': last_update['available']}
                else:
                    wallet_dict[coin] = {'balance': 0, 'available': 0}
        except:
            print('Conection failed')

        return wallet_dict

    def new_wallet_snapshot (self, doc_data :dict):
        try:
            doc_data['uid'] = self.uid
            if doc_data['currency'] not in self.coins():
                print('Currency is not available in coins, it will be added')
                self.update_one(coin = doc_data['currency'])
                print('Currency added to coins successfully')

            new_wallet_snapshot (col = self.col_wallets, doc_data = doc_data)
        except:
            print('Conection failed')

    def available (self, currency: str):
        try:
            wallet = self.wallet_info()
            if currency in wallet:
                available = wallet[currency]['available']
            else:
                print(f'Currency {currency} is not active')
                available = 0
            return available
        except:
            print('Could not access wallet information')

    def amount (self, currency: str):
        try:
            wallet = self.wallet_info()
            if currency in wallet:
                available = wallet[currency]['amount']
            else:
                print(f'Currency {currency} is not active')
                available = 0
            return available
        except:
            print('Could not access wallet information')

    #Offers methods.
    def new_offer (self, offer_data: dict):
        offer_data['uid'] = self.uid
        new_offer(self.col_offers, offer_data)

    def offer_status(self, offer_id: int):
        status = offer_status (col = self.col_offers, offer_id = offer_id)
        return status

    def change_offer_status (self, offer_id: int,
                         closed_date = None, was_executed = None ):
        change_offer_status (col = self.col_offers, offer_id = offer_id,
                         closed_date = closed_date, was_executed = was_executed)

    def open_offers (self):
        list_open_offers = list(self.col_offers.find({'closed_date': 0}))
        print(list_open_offers)
        return list_open_offers

    #Credits methods.
    def new_credit (self, credit_data: dict):
        credit_data['uid'] = self.uid
        new_credit(self.col_credits, credit_data)

    def credit_status(self, credit_id: int):
        end_date = credit_status (col = self.col_credits, credit_id = credit_id)
        return end_date

    def change_credit_status (self, credit_id: int, end_date = None,
                              earn_money = None, paid_fees = None):
        change_credit_status (col = self.col_credits, credit_id = credit_id,
                              end_date = end_date, earn_money = earn_money,
                              paid_fees = paid_fees)

    def open_credits (self):
        list_open_credits = list(self.col_credits.find({'end_date': 0}))
        print(list_open_credits)
        return list_open_credits

#General functions.
def mongo_db_conection (mongo_user: str, mongo_password: str,
                        mg_user_info = False) -> pymongo.MongoClient:
    """
    Parameters
    ----------
    mongo_user : str
    mongo_password : str
    mg_user_info : TYPE, optional
        The default is False.

    Conects to 'FundingBot' cluster by user and password.
    Recieve mongo user and password from connection method 'Connect to your aplication'.
    Returns instance of a class MongoClient.
    Prints a list of databases available and collections if mg_user_info = True.

    Returns
    -------
    client : pymongo.MongoClient
    If connection fails, it returns NoneType object.
    """

    try:
        #Connection string generated to get access to 'FundingBot' cluster.
        client = pymongo.MongoClient("mongodb+srv://FundingBot:{}@fundingbot-bnota.mongodb.net/{}?retryWrites=true&w=majority".format(mongo_password,mongo_user))
        if mg_user_info:
            list_db_available = client.list_database_names()
            print(f'Data bases available in \"{mongo_user}\" = ', list_db_available)
            print('')
            for db in list_db_available:
                collections_list = client[db].list_collection_names()
                print("Collections avialable in database \"{}\": {}".format(db, collections_list))
                print('')
    except:
        client = None
        print('Conection Failed, return = None')
        print('')

    return client

def insert_document (client: pymongo.MongoClient, db_name: str,
                     col_name :str, doc_data :dict):
    """
    Parameters
    ----------
    client : pymongo.MongoClient
    db_name : str
    col_name : str
    doc_data : dict

    Inserts doc_data in client.db_name.col_name.

    Returns
    -------
    None.
    """
    try:
        db = client[db_name]
        col = db[col_name]
        col.insert_one(doc_data)
        print('Document inserted successfully')
        print('')
    except:
        print('Error inserting document')
        print('')

def new_bot_user (client: pymongo.MongoClient, user_data: dict):
    """
    Parameters
    ----------
    client : pymongo.MongoClient
    user_data : dict
        Dictionary with keys: ['name', 'surname', 'user_name', 'uid', 'API_key',
                               'API_secret', 'coins', 'timestamp', 'is_active',
                               'start_amount', 'earnings', 'current_amount']

    Creates new document in db = 'funding_bfx', col = 'users'
    with new user data.

    Returns
    -------
    None.

    """
    try:
        #Checks if client already exists.
        if client.funding_bfx.users.find_one({'uid': user_data['uid']}):
            uid = user_data['uid']
            print(f'User with uid: {uid} already exists')
            print('')
            return
        else:
            print('Inserting new user data in users_data')
            insert_document(client, 'funding_bfx', 'users', user_data)
    except:
        print('New user could not be created')
        print('')

def new_wallet_snapshot (col: pymongo.collection, doc_data :dict):
    """
    Parameters
    ----------
    col : pymongo.collection
        Collection where wallets snapshots are being store.
    doc_data : dict
        Dictionary with keys: ['uid', 'timestamp', 'currency', 'amount',
                               'available', 'rate_curr_usd']

    Returns
    -------
    None.
    """
    try:
        col.insert_one(doc_data)
    except:
        print('Snapshot could not be saved')

def new_offer (col: pymongo.collection, offer_data: dict):
    """
    Saves offer data in collection specified.
    """
    try:
        #Search if offer with offer_id already exists.
        col.insert_one(offer_data)
    except:
        print('Offer could not be saved')

def offer_status (col: pymongo.collection, offer_id: int):
    """
    Checks status, returns a tuple.
    """
    try:
        offer = col.find_one({'offer_id': offer_id})
        closed_date = offer['closed_date']
        was_executed = offer['was_executed']
        print(f'Offers closed_date value is {closed_date}')
        print(f'Offers was_executed value is {was_executed}')
        status = (closed_date, was_executed)
    except:
        print('Offer not found')
        status ('Not_Found', 'Not_found')
    return status

def change_offer_status (col: pymongo.collection, offer_id: int,
                         closed_date = None, was_executed = None):
    """
    Changes closed_date and/or was_executed

    """
    try:
        if col.find_one({'offer_id': offer_id}):
            if closed_date:
                col.update_one({'offer_id': offer_id},
                                    {"$set":
                                        {'closed_date':
                                             closed_date}
                                    }
                               )
            if was_executed:
                col.update_one({'offer_id': offer_id},
                                    {"$set":
                                        {'was_executed':
                                             was_executed}
                                    }
                               )
        else:
            print('Offer not found')
    except:
        print('Offer status could not be changed')

def new_credit (col: pymongo.collection, credit_data: dict):
    """
    Saves credit data in collection specified.
    """
    try:
        col.insert_one(credit_data)
    except:
        print('Credit could not be saved')

def credit_status (col: pymongo.collection, credit_id: int):
    """
    Checks status, returns a tuple.
    """
    try:
        credit = col.find_one({'credit_id': credit_id})
        end_date = credit['end_date']
        print(f'Offers closed_date value is {end_date}')
        return end_date
    except:
        print('Credit not found')
        return 'Not_Found'

def change_credit_status (col: pymongo.collection, credit_id: int,
                          end_date = None, earn_money = None,
                          paid_fees = None):
    """
    Changes end_date
    """
    try:
        if col.find_one({'credit_id': credit_id}):
            if end_date:
                col.update_one({'credit_id': credit_id},
                                    {"$set":
                                        {'end_date':
                                             end_date}
                                    }
                               )
            if earn_money:
                col.update_one({'credit_id': credit_id},
                                    {"$set":
                                        {'earn_money':
                                             earn_money}
                                    }
                               )
            if paid_fees:
                col.update_one({'credit_id': credit_id},
                                    {"$set":
                                        {'paid_fees':
                                             paid_fees}
                                    }
                               )
        else:
            print('Credit not found')
    except:
        print('Credit status could not be changed')
