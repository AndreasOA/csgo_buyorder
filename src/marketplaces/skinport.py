import base64
from this import d
import requests
import time
import pandas as pd
from json import JSONDecodeError
from requests_ip_rotator import ApiGateway
from selenium import webdriver


def authentication(clientId, clientSecret):
    clientData = f"{clientId}:{clientSecret}"
    encodedData = str(base64.b64encode(clientData.encode("utf-8")), "utf-8")
    authorizationHeaderString = f"Basic {encodedData}"

    return clientData, encodedData, authorizationHeaderString


def sp_get_marketplace_items(session):
    return session.get("https://api.skinport.com/v1/items", params={
        "app_id": 730,
        "currency": "EUR",
        "tradable": 0
    }).json()


def save_data_to_txt(data):
    f = open('gen_files/skinport.txt', 'w')
    f.write(data)
    f.close()


def filter_data(data, accepted_items, acceptable_discount, type):
    try:
        x = data['market_hash_name']
    except KeyError as ke:
        print(data)
        time.sleep(300)
        return pd.DataFrame()

    accepted_data = data[data['market_hash_name'].isin(accepted_items)].reset_index(drop=True)

    mask_rare = accepted_data['market_hash_name'].str.contains(r'★', na=True)
    data_rare = accepted_data[mask_rare]
    data_not_rare = accepted_data[~mask_rare]

    if type == 'sb':
        min_price = 'min_price_sb'
    elif type == 'sp':
        min_price = 'min_price'

    data_rare_dc = data_rare[((data_rare[min_price]/data_rare['suggested_price'] < (acceptable_discount + 0.08)) & (data_rare["suggested_price"] > 400.0)) | 
                            (data_rare[min_price]/data_rare['suggested_price'] < acceptable_discount)]
    data_rare_dc = data_rare_dc[data_rare_dc[min_price].notna()]
    data_not_rare_dc = data_not_rare[(data_not_rare[min_price]/data_not_rare['suggested_price'] < acceptable_discount)]
    data_not_rare_dc = data_not_rare_dc[data_not_rare_dc[min_price].notna()]

    return pd.concat([data_rare_dc, data_not_rare_dc])
    

def buy_sp_item(link_sp, price_db):
    driver = webdriver.Chrome(r'chromedriver')
    driver.get(link_sp)
    item_price = driver.find_element_by_class_name("ItemPage-value")
    item_price = float(item_price.find_element_by_tag_name('div').text.replace("€", "").replace(",", ".").replace(" ", ""))
    if item_price == price_db:
        add_to_cart = driver.find_elements_by_class_name("SubmitButton")
        add_to_cart.click()
        driver.get("https://skinport.com/de/cart")
        checkboxes = driver.find_elements_by_class_name("Checkbox-input")
        for checkbox in checkboxes:
            checkbox.click()
        buy_button = driver.find_elements_by_class_name("SubmitButton")
        buy_button.click()




