import pandas as pd
import pymongo 
from datetime import datetime

class Bot_user:
    """
    Before creating an instance of the class, user need to be registered in
    proyect "FundingBot", database "funding_bot", collection 'users_data' as 
    a document. 
    If client is not registered it returns None.
    """
    def __init__(self, client: pymongo.MongoClient, user_dni: int):
        """
        Gets the data of the user from users_data document.
        """ 
        self.client = client
        self.user_dni = user_dni                      
        #Checks if conection was successful, gets client data form users_data 
        try:
            self.col_data = self.client.funding_users.users_data            
            self.user_data = self.col_data.find_one({'dni': self.user_dni})
            self.name = self.user_data['name']
            self.surname = self.user_data['surname']
            self.dni = self.user_data['dni']
            self.API_key = self.user_data['API_key']
            self.API_secret = self.user_data['API_secret']
            self.start_date = self.user_data['start_date']
            self.start_amount = self.user_data['start_amount']    
            #Database and collections name where historical data is stored.
            self.db_records_name = self.user_data['data_base']    
            self.db_records = self.client[self.db_records_name]
            self.col_wallet = self.db_records['wallet']
            self.col_offers = self.db_records['offers']
            self.col_credits = self.db_records['credits']
        except:
            self.col_data = None
            self.user_data = None
            self.name = None
            self.surname = None
            self.dni = None
            self.API_key = None
            self.API_secret = None
            self.start_date = None
            self.start_amount = None
            self.db_records_name = None
            self.db_records = None
            self.col_wallet = None
            self.col_offers = None
            self.col_credits = None            
            print('User :',self.user_dni, 'not found')
        
    ##Methods associated with the class        
    def update (self):
        """
        Method to update modified values from database by other functions.
        """
        self.__init__(self.client, self.user_dni)
    
    #Status info methods.
    def is_active(self):
        return self.col_data.find_one({'dni': self.user_dni})['is_active']
    
    def earnings(self):
        return self.col_data.find_one({'dni': self.user_dni})['earnings']    
    
    def current_amount(self):
        return self.col_data.find_one({'dni': self.user_dni})['current_amount']
    
    def update_one(self, **kwargs):
        try:
            for key, value in kwargs.items():
                self.col_data.update_one({'dni': self.dni},
                            {"$set":
                                {key: value}
                            }
                                   )
        except:
            print('Update could not be performed')
        
    #Wallet methods.    
    def wallet_info (self):
        wallet_list = list(self.col_wallet.find({}))
        print(wallet_list)
        return wallet_list
    
    def new_currency (self, symbol: str, description: str, start_amount = 0):                    
        if self.col_wallet.find_one({'symbol': symbol}):
            print('Currency already exists')
        else:
            new_currency (col = self.col_wallet, symbol = symbol, description = description,
                          start_amount = start_amount)
            
    def available (self, symbol: str):
        try:
            if self.col_wallet.find_one({'symbol': symbol}):
                available = self.col_wallet.find_one({'symbol': symbol})['available_' + symbol]      
                print('available_' + symbol + ':', available)
                return available
            else:
                print('Currency not found')
        except:
            print('Could not access wallet information')
            
    def update_wallet (self, symbol: str, new_amount: int):
        if self.col_wallet.find_one({'symbol': symbol}):
            update_wallet(col = self.col_wallet, symbol = symbol, new_amount = new_amount) 
        else: 
            print(f'Currency does not exists in {self.name} {self.surname} wallet')
        
    #Offers methods.
    def new_offer (self, offer_data: dict):
        new_offer(self.col_offers, offer_data)
        
    def offer_status(self, id_offer: int):
        status = offer_status (col = self.col_offers, id_offer = id_offer)
        return status
    
    def change_offer_status (self, id_offer: int, 
                         closed_date = None, was_executed = None ):
        change_offer_status (col = self.col_offers, id_offer = id_offer, 
                         closed_date = closed_date, was_executed = was_executed)
    
    def open_offers (self):
        list_open_offers = list(self.col_offers.find({'closed_date': 0}))
        print(list_open_offers)
        return list_open_offers
    
    #Credits methods.
    def new_credit (self, credit_data: dict):
        new_credit(self.col_credits, credit_data)
        
    def credit_status(self, id_credit: int):
        end_date = credit_status (col = self.col_credits, id_credit = id_credit)
        return end_date
    
    def change_credit_status (self, id_credit: int, end_date = None):
        change_credit_status (col = self.col_credits, id_credit = id_credit, 
                              end_date = end_date)
    
    def open_credits (self):
        list_open_credits = list(self.col_credits.find({'end_date': 0}))
        print(list_open_credits)
        return list_open_credits  
        
#General functions.        
def mongo_db_conection (mongo_user: str, mongo_password: str, 
                        mg_user_info = False) -> pymongo.MongoClient:
    """
    Recieve mongo data base proyect name and password.
    Returns instance of a class MongoClient.
    Prints a list of databases available and collections if mg_user_info = True.   
    """
    #If connection fails, it returns NoneType object.
    try:
        client = pymongo.MongoClient("mongodb+srv://FundingBot:{}@fundingbot-ncgso.mongodb.net/{}?retryWrites=true&w=majority".format(mongo_password,mongo_user))
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
        
    return client    
    
def insert_document (client: pymongo.MongoClient, db_name: str, 
                     coll_name :str, doc_data :dict):
    try:
        db = client[db_name]
        coll = db[coll_name]
        coll.insert_one(doc_data)        
        print('Document inserted successfully')
        print('')
    except:
        print('Error inserting document')        
        print('')
    
def new_bot_user (client: pymongo.MongoClient, user_data: dict):
    """Creates new document in db = 'user_name' + 'id_user', coll = 'users_data'
       with new user data.
       Crete empty collections 'wallet', 'offers' and 'credits'.       
    """
    try:
        #Define the database name with user_data values.
        db_name = user_data['name'][0:2] + user_data['surname'][0:1] + '_' + str(user_data['dni'])[-3:]
        user_data['data_base'] = db_name        
        #Checks if client already exists.
        if client.funding_users.users_data.find_one({'dni': user_data['dni']}):        
            print('User already exists')    
            return 
        else:
            print('Inserting new user data in users_data')
            insert_document(client, 'funding_users', 'users_data', user_data)              
    except:
        print('New user could not be created')

def new_currency (col: pymongo.collection, symbol: str, description: str,
                  start_amount = 0):
    """
    Creates document in user collection 'wallet'.
    """ 
    try:
        #Search if document with symbol already exists.
        if col.find_one({'symbol': symbol}):
            print(f'Currency {symbol} already exists')
        else:
            available_symbol = 'available_' + symbol        
            col.insert_one({'symbol': symbol,
                            'description': description,
                            available_symbol: start_amount})       
    except:
        print('Currency could not be created')
                
def update_wallet (col: pymongo.collection, symbol: str, new_amount: int):
    """
    Updates wallet information in user collection 'wallet'.
    If currency doesn't exists, prints error message.
    """  
    try:    
        if col.find_one({'symbol': symbol}):
            data_dir = 'available' + '_' + symbol
            #Wallet is document with id = 1 in collection 'user name' + 'id_user'
            col.update_one({'symbol': symbol},
                                {"$set":
                                    {data_dir:
                                         new_amount}
                                }
                           )
        else:
            print('Currency does not exist')
    except:
        print('Wallet could not be updated')

def new_offer (col: pymongo.collection, offer_data: dict):
    """
    Saves offer data in collection specified.
    """
    try:   
        #Search if offer with id_offer already exists.
        offer_id = offer_data['id_offer']
        if col.find_one({'id_offer': offer_id}):
            print(f'Offer {offer_id} already exists')
        else:                  
            col.insert_one(offer_data)       
    except:
        print('Offer could not be saved')
                
def offer_status (col: pymongo.collection, id_offer: int):
    """
    Checks status, returns a tuple.
    """    
    try:
        offer = col.find_one({'id_offer': id_offer})
        closed_date = offer['closed_date']
        was_executed = offer['was_executed']
        print(f'Offers closed_date value is {closed_date}')
        print(f'Offers was_executed value is {was_executed}')
        status = (closed_date, was_executed) 
    except:
        print('Offer not found')
        status ('Not_Found', 'Not_found')
    return status
        
        
def change_offer_status (col: pymongo.collection, id_offer: int, 
                         closed_date = None, was_executed = None):
    """
    Changes closed_date and/or was_executed

    """
    try:
        if col.find_one({'id_offer': id_offer}):
            if closed_date:
                col.update_one({'id_offer': id_offer},
                                    {"$set":
                                        {'closed_date':
                                             closed_date}
                                    }
                               )
            if was_executed:
                col.update_one({'id_offer': id_offer},
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
        #Search if offer with id_offer already exists.
        credit_id = credit_data['id_credit']
        if col.find_one({'id_credit': credit_id}):
            print(f'Credit {credit_id} already exists')
        else:                  
            col.insert_one(credit_data)       
    except:
        print('Credit could not be saved')
        
def credit_status (col: pymongo.collection, id_credit: int):
    """
    Checks status, returns a tuple.
    """    
    try:
        credit = col.find_one({'id_credit': id_credit})
        end_date = credit['end_date']
        print(f'Offers closed_date value is {end_date}')
        return end_date
    except:
        print('Credit not found')
        return 'Not_Found'
    
def change_credit_status (col: pymongo.collection, id_credit: int, 
                          end_date = None):
    """
    Changes end_date
    """
    try:
        if col.find_one({'id_credit': id_credit}):
            if end_date:
                col.update_one({'id_credit': id_credit},
                                    {"$set":
                                        {'end_date':
                                             end_date}
                                    }
                               )
        else:
            print('Credit not found')
    except:
        print('Credit status could not be changed')    