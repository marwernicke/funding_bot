from bfxapi import Client

def conect(API_KEY, API_SECRET):
    bfx = Client(API_KEY, API_SECRET)
    return(bfx)
