from bs4 import BeautifulSoup
from src.constants import *
import time


def get_buyorder(item_name, d, cr):
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
