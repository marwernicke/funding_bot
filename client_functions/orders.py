async def create_funding(amount,per,rate,coin,bfx):
  response = None
  try:
      response = await bfx.rest.submit_funding_offer('f{}'.format(coin), amount, rate, per)
  except Exception as e:
      print('Couldnt create funding offers: '+ str(e))
  if response != None:
      print ("NEW Offer: ", response.notify_info)
      id = vars(response.notify_info)['id']
      return(id)
  else:
      return(None)

async def cancel_all_offers():
    remove = []
    for offer in billetera.bot.offers:
        try:
            response = await bfx.rest.submit_cancel_funding_offer(offer)
            remove.append(offer)
        except Exception as e:
            print('Couldnt cancel funding offers: '+ str(e))
    for o in remove:
        billetera.bot.remove(o, where="offers")
