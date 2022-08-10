import requests
import enum
import json

SPACE_SYMBOL = '%20'
SPLITTER_SYMBOL = '%7C'
LEFT_BRACKET_SYMBOL = '%28'
RIGHT_BRACKET_SYMBOL = '%29'

class AppId(enum.Enum):
  CSGO = 730

class Currency(enum.Enum):
  USD = 1 # United States Dollars
  UKP = 2 # United Kingdom Pounds
  EUR = 3 # European Euros
  CHF = 4 # Swiss Franc
  RUB = 5 # Russian Roubles
  POL = 6 # Polish złoty 
  BZL = 7 # Brazilian real
  JAP = 8 # Japanese Yen
  SWD = 9 # Swedish Krona
  IND = 10 # Indonesian Rupiah
  MAL = 11 # Malaysian Ringgit
  
class MarketItem():
  sucess = False
  lowest_price = 0.0
  median_price = 0.0
  name = ""
  volume = 0
  
def GetMarketItem(appid, name, currency = Currency.EUR.value):
  strdat = ""
  Item = MarketItem()
  name = name.replace(' ', SPACE_SYMBOL).replace('|', SPLITTER_SYMBOL).replace('(', LEFT_BRACKET_SYMBOL).replace(')',RIGHT_BRACKET_SYMBOL)
  url = "http://steamcommunity.com/market/priceoverview/?appid=%s&currency=%s&market_hash_name=" % (appid, currency) + name
  steam_dat = requests.get(url)

  data = json.loads(steam_dat.read().decode())
  strdat = str(data)
  Item.name = name.replace("+", " ").replace("StatTrak%E2%84%A2 ", "StatTrak ")
  if (strdat.find("success': True") != -1):
    Item.sucess = True
  if (strdat.find('median_price') != -1):
    Item.median_price = data['median_price']
  if (strdat.find('lowest_price') != -1):
    Item.lowest_price = data['lowest_price']
  if (strdat.find('volume') != -1):
    Item.volume = data['volume']
  return Item

def PrintMarketItem(it, volume = False):
  if (len(it.name) > 0):
    print(it.name + ": ")
  if (len(it.median_price) > 0):
    print(it.median_price)
  elif (len(it.lowest_price) > 0):
    print(it.lowest_price)
  else:
    print("No valid price found!")
  if (volume and len(it.volume) > 0):
    print(it.volume)
# - # - # - # - # - # - # - # - # -# - # - # - # - # - # - # - # - # - #
if __name__ == '__main__':
  PrintMarketItem(GetMarketItem(AppId.CSGO.value, ST + "AWP | PAW" + FN), 3)