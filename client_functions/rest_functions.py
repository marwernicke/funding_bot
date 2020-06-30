"""
Module with functions to conect to bitfinex API REST endpoints.
"""

def get_exchange_rate(ccy1: str, ccy2 = 'USD') -> int:
    """
    Parameters
    ----------
    ccy1 : str
        First exchange currency to get the forex rate.
    ccy2 : TYPE, optional
        Second exchange currency. The default is 'usd'.

    Returns
    -------
    int
        returns the ratio ccy1 / ccy2
    """
    try:
        url = 'https://api.bitfinex.com/v2/calc/fx'
        json_data = {
                     'ccy1': ccy1.upper(),
                     'ccy2': ccy2.upper()
                     }
        request = requests.post(url, json = json_data)
        response = request.json()
        forex_rate = response[0]
        if forex_rate == 'error':
             print(f'Couldnt get foreign exchange ratio, returned 0.')
             forex_rate = 0

        return forex_rate
    except Exception as e:
        print(f'Couldnt get foreign exchange ratio:\n{str(e)}')
