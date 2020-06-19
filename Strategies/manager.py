from Strategies import rolling_high
from client_functions import orders

async def balance_available(user, coin:str, amount:float):
    """creates a new funding offer, firts it uses a strategy to determine parameters, then it sends the order to bitfinex"""
    rate, per = await rolling_high.strategy(coin)
    rate= 0.005
    amount= 500
    offer_id = await orders.create_funding(amount, per, rate, coin, user)
