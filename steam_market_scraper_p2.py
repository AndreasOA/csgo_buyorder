from dataclasses import replace
from requests_html import HTML
from requests_html import AsyncHTMLSession
from requests_html import HTMLSession

session = HTMLSession()

SPACE_SYMBOL = '%20'
SPLITTER_SYMBOL = '%7C'


item_name = '★%20Talon%20Knife%20%7C%20Rust%20Coat%20%28Battle-Scarred%29'


r = session.get('https://steamcommunity.com/market/listings/730/' + item_name)
r.html.render(timeout=1000)
about = r.html.find('#market_commodity_buyrequests')
print(about[0].find('.market_commodity_orders_header_promote'))
print(r.html.html.split('market_commodity_buyrequests')[1].split('div')[0])

#session.run(get_steammarket_item_page(item_name))
# Urli request gives count XX offers. Easy way for lowest offer
urli = 'https://steamcommunity.com/market/listings/730/' + item_name + '/render?start=0&count=5&currency=5&language=english'
print(urli)
#r = asession.get(urli)
