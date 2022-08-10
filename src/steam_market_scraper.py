import urllib.request, json, urllib.error
import enum
ST = "StatTrak%E2%84%A2 "
FN = " (Factory New)"
MW = " (Minimal Wear)"
FT = " (Field-Tested)"
WW = " (Well-Worn)"
BS = " (Battle-Scarred)"
SOUVENIR = "Souvenir "
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
  lowest_price = ""
  median_price = ""
  name = ""
  volume = 0
def GetMarketItem(appid, name, currency = Currency.USD.value):
  strdat = ""
  Item = MarketItem()
  name = name.replace(" ", "+")
  try:
    url = urllib.request.urlopen("http://steamcommunity.com/market/priceoverview/?appid=%s&currency=%s&market_hash_name=" % (appid, currency) + name)
    data = json.loads(url.read().decode())
    strdat = str(data)
    Item.name = name.replace("+", " ").replace("StatTrak%E2%84%A2 ", "StatTrak ")
  except urllib.error.URLError as e:
    print("ERROR: %s" % e.reason)
    return MarketItem()
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
PrintMarketItem(GetMarketItem(AppId.CSGO.value, ST + "AWP | PAW" + FN), False)


# market_commodity_orders_header_promote

