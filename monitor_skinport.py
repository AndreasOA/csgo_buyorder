from src.marketplaces.skinport.skinport_selenium import *
import json


f = open("misc/credentials_adv.json")
data = json.load(f)
f.close()

t_api = data['telegram']['api_token']
t_id = data['telegram']['chat_id']
phone = ''

skinportMarketTracker = Skinport(username = data['skinport_api_credentials']['username'], 
                                 password = data['skinport_api_credentials']['password'],
                                 language = 'GB',
                                 ccs = data['cc']['secret'], 
                                 telegram_api = t_api,
                                 telegram_chat = t_id,
                                 phone = phone,
                                 acceptable_discount = 0.25,
                                 good_discount = 0.3,
                                 debug = True, 
                                 buy_item = True,
                                 notify_user = True
                                )

skinportMarketTracker.runMarketTracker()