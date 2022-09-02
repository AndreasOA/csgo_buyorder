from json import JSONDecodeError
from src.marketplaces.skinbaron import *
from src.marketplaces.skinport import *
from src.find_profit_items import *
from src.calc_resell_pot import *
from src.discord_msg import *
import time
import pandas as pd
import requests


def fix_suggested_price(row: pd.Series) -> float:
    suggested_price = row['suggested_price']
    if 'Doppler' in row['market_hash_name'] or 'Marble' in row['market_hash_name']:
        suggested_price = ((row['min_price_sb'] + row['min_price']) / 2) * 1.25

    return suggested_price


def sb_sp_merge(row: pd.Series, df_sb: pd.DataFrame) -> pd.Series:
    try:
        name_sp, condition_sp = row['market_hash_name'].split(' (')
        condition_sp = condition_sp.replace(')', '').upper().replace(' ', '_').replace('-','_')
        df_sb['name'] + ' (' + df_sb['exterior'] + ')'
        return df_sb[   (df_sb['name'] == name_sp) & 
                        (df_sb['exterior'] == condition_sp) & 
                        (df_sb['statTrak'] == False) & 
                        (df_sb['souvenir'] == False)
                    ]['lowestPrice'].to_list()[0]
    except (IndexError, ValueError) as e:
        return row['min_price']


def rename_item(x):
    try:
        return x['market_hash_name'].split(' (')[0]
    except (IndexError, ValueError) as e:
        return ""


def rename_condition(x):
    try:
        return x['market_hash_name'].split(' (')[1].replace(')', '').upper().replace(' ', '_').replace('-','_')
    except (IndexError, ValueError) as e:
        return ""


def define_profit(row: pd.Series) -> list:
    marketplace = ''
    if row['min_price'] == 0.00 or row['min_price_sb'] == 0.00:
        return -1.00
    else:
        if row['min_price'] <  row['min_price_sb']:
            marketplace = 'sp'
            buy_price = row['min_price']
            min_price_om = row['min_price_sb']
        else:
            marketplace = 'sb'
            buy_price = row['min_price_sb']
            min_price_om = row['min_price']
        
        return calc_resell_pot(marketplace, buy_price, min_price_om)



def get_current_skinport_data(accepted_items: list, acceptable_discount: float, session) -> list:
    run_cnt = 0
    sent_msg = []
    while True:
        if run_cnt % 50 == 0:
            requests.get(URL+'[SKINPORT] -  STILL RUNNING').json()
        # Update Skinport Data
        print('[SKINPORT] - Fetching data')
        start_time = time.time()
        try:
            df_sp = pd.DataFrame.from_records(sp_get_marketplace_items(session))
        except (JSONDecodeError, ValueError) as je:
            print('[SKINPORT] - Request failed')
            time.sleep(30)
            continue

        data_filteted = filter_data(df_sp, accepted_items, acceptable_discount, 'sp')

        for i, item in data_filteted.iterrows():
            skins_data = {'item_name': item['market_hash_name'],'suggested_price': item['suggested_price'],'min_price': item['min_price'],'link': item['item_page']}
            msg = getDiscordMsg2(skins_data)

            if msg != '' and msg not in sent_msg:
                requests.get(URL+msg).json()
                sent_msg.append(msg)
                print('Offer found. ApeBot doing ape things.')
        run_cnt += 1
        print(time.time()- start_time)
        time.sleep(12)


def get_current_skinbaron_data(api_key: str, accepted_items: list, acceptable_discount: float, session) -> list:
    run_cnt = 0
    sent_msg = []
    while True:
        if run_cnt % 20 == 0:
            requests.get(URL+'[SKINBARON] -  STILL RUNNING').json()
        # Update Skinport Data
        print('[SKINBARON] - Fetching data')
        start_time = time.time()

        try:
            df_sp = pd.DataFrame.from_records(sp_get_marketplace_items(session))
            df_sp['name'] = df_sp.apply(lambda x: rename_item(x), axis = 1)
            df_sp['condition'] = df_sp.apply(lambda x: rename_condition(x), axis = 1)
        except JSONDecodeError as je:
            print('[SKINPORT] - Request failed')
            time.sleep(30)
            continue

        df_sp = df_sp[df_sp['market_hash_name'].isin(accepted_items)].reset_index(drop=True)
        df_sp = df_sp[df_sp['suggested_price'].notna()]


        for i, item in df_sp.iterrows():
            acceptable_discount_temp = acceptable_discount
            if item['market_hash_name'].find('★ ') != -1 and item["suggested_price"] > 400.0:
                acceptable_discount_temp = acceptable_discount + 0.08

            name_query, name_condition = item['market_hash_name'].replace('★ ', '').split(' (')
            name_condition = name_condition.replace(')', '')
            try:
                skinbaron_data = str(get_marketplace_items(name_query, api_key)).replace('},', '},\n')
            except JSONDecodeError as je:
                continue
            formatted_skinbaron_data = format_skinbaron_data(skinbaron_data, name_condition)
            id_nr, name_sb, min_price_sb, me_, ma_, q_, item_page_sb = formatted_skinbaron_data
            min_price_sb = float(min_price_sb)
            item_page_sb = item_page_sb.replace("'", '')
            price_perc = ((min_price_sb * ( 1 + SB_BUY_FEE_SOFORT))/item["suggested_price"])
            if ( price_perc < acceptable_discount_temp) and 'Souvenir' not in name_sb and min_price_sb != 0.0:
                skins_data = {'item_name': item['market_hash_name'],'suggested_price': item['suggested_price'],'min_price': min_price_sb* ( 1 + SB_BUY_FEE_SOFORT),'link': item_page_sb}
                msg = getDiscordMsg2(skins_data)

                if msg != '' and msg not in sent_msg:
                    sent_msg.append(msg)
                    print('Offer found. ApeBot doing ape things.')
                    requests.get(URL+msg).json()
        
        run_cnt += 1
        print(time.time()- start_time)