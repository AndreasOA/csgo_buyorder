import requests
import json


def get_marketplace_items(item_name, api_key):
    headers = {
        'x-requested-with': 'XMLHttpRequest',
    }
    json_data = {
        'apikey': api_key,
        'appid': 730,
        'search_item': item_name,
        'items_per_page': 50
    }
    return requests.post('https://api.skinbaron.de/Search', headers=headers, json=json_data).json()


def buy_marketplace_item(api_key, item_id, total_price):
    headers = {
        'x-requested-with': 'XMLHttpRequest',
    }
    json_data = {
        "apikey": api_key,
        "total": total_price,
        "toInventory": true,
        "saleids": [item_id]
        }
    return requests.post('https://api.skinbaron.de/BuyItems', headers=headers, json=json_data).json()


def get_marketplace_list(api_key):
    headers = {
        'x-requested-with': 'XMLHttpRequest',
    }
    json_data = {
        "apikey": api_key,
        "appId": 730
    }
    return requests.post('https://api.skinbaron.de/GetExtendedPriceList', headers=headers, json=json_data).json()


def save_data_to_txt(data):
    f = open('gen_files/skinbaron.txt', 'w')
    f.write(data)
    print(data)
    f.close()


def format_skinbaron_data(data, condition):
    id_nr = ''
    filtered_list = []
    min_price = 99999999
    max_price = 0
    mean_price = 0
    nr_items = 0
    shop_page = ''
    name = ''
    shop_page = ''

    for line in data.split('\n')[1:]:
        line = line.split('{')[1].split('}')[0]
        filtered_list = [elem.split(': ')[1] for elem in line.split(", '")]
        try:
            id_nr, price, img, name, inspect_page, \
                inspect, stickers, float_cond, app_id = filtered_list
        except ValueError as ve:
            id_nr, price, img, name, inspect_page, \
                inspect, stickers, app_id = filtered_list
        if condition in name:
            nr_items += 1
            price = float(price)
            if price < min_price:
                min_price = price
                shop_page = inspect_page
            if price > max_price:
                max_price = price
            mean_price += price

    try:
        mean_price /= nr_items
    except ZeroDivisionError as e:
        min_price = 0
        max_price = 0
        mean_price = None

    return id_nr, name, str(min_price), str(mean_price), str(max_price), str(nr_items), shop_page


if __name__ == '__main__':
    f = open("credentials.json")
    data = json.load(f)
    #print(format_skinbaron_data(str(get_marketplace_items('Ursus Knife | Tiger Tooth', data['skinbaron_api_credentials']['api_key'])).replace('},', '},\n'), 'Factory New'))
    print(str(get_marketplace_list(data['skinbaron_api_credentials']['api_key'])))