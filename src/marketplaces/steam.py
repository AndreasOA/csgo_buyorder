from bs4 import BeautifulSoup
from src.constants import *
import time
import requests
import json


def GetMarketItemSel(item_name: str, d, cr):
    item_name = item_name.replace(' ', SPACE_SYMBOL).replace('|', SPLITTER_SYMBOL).replace('(', LEFT_BRACKET_SYMBOL).replace(')',RIGHT_BRACKET_SYMBOL)

    urli = 'https://steamcommunity.com/market/listings/730/' + item_name
    d.get(urli)
    time.sleep(2)

    run = 0
    while True:
        try:
            html = d.page_source
            soup = BeautifulSoup(html)
            buy_order = str(soup.html).split('market_commodity_orders_header_promote">$')[1].split('</span')[0]
            break
        except IndexError as ie:
            run += 1
            time.sleep(0.2)
            if run == 5:
                buy_order ='0.0'
                break
    conv_rate = cr.get_rate('USD', 'EUR')
    return float(buy_order.replace(',',''))*conv_rate * 0.85


def GetMarketItemReq(name, steam_conn):
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

