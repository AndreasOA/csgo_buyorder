import requests
import time
import json

SPACE_SYMBOL = '%20'
SPLITTER_SYMBOL = '%7C'
LEFT_BRACKET_SYMBOL = '%28'
RIGHT_BRACKET_SYMBOL = '%29'

def GetMarketItem(name, steam_conn):
  name = name.replace(' ', SPACE_SYMBOL).replace('|', SPLITTER_SYMBOL).replace('(', LEFT_BRACKET_SYMBOL).replace(')',RIGHT_BRACKET_SYMBOL)
  url = "http://steamcommunity.com/market/priceoverview/?appid=%s&currency=%s&market_hash_name=" % (730,3) + name
  if not steam_conn:
    return 0.0, 'https://steamcommunity.com/market/listings/730/' + name, steam_conn

  steam_dat = requests.get(url)
  time.sleep(2)
  data = json.loads(steam_dat.content.decode())
  try:
    return float(data['lowest_price'].replace('€', '').replace(',', '.').replace('-', '0').replace(' ', '')), 'https://steamcommunity.com/market/listings/730/' + name, True
  except (KeyError, requests.exceptions.ConnectionError) as e:
    return 0.0, 'https://steamcommunity.com/market/listings/730/' + name, steam_conn
  except TypeError as te:
    return 0.0, 'https://steamcommunity.com/market/listings/730/' + name, False
