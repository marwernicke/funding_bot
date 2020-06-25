async def create_funding(amount,per,rate,coin,user):
  response = None
  try:
      response = await user.bfx.rest.submit_funding_offer('f{}'.format(coin), amount, rate, per)
  except Exception as e:
      print('Couldnt create funding offers: '+ str(e))
  if response != None:
      print ("NEW Offer: ", response.notify_info)
      id = vars(response.notify_info)['id']
      return(id)
  else:
      return(None)

async def cancel_all_offers(user):
    print('canceling offers')
    offers_to_cancel = user.offers.copy()
    for offer in offers_to_cancel:
        try:
            response = await user.bfx.rest.submit_cancel_funding_offer(offer)
        except Exception as e:
            print('Couldnt cancel funding offers: '+ str(e))
