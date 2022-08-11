from posixpath import split
from src.skinbaron_get_marketpalce_data import *
from src.skinport_get_marketplace_data import *
from src.find_profit_items import *
from src.calc_resell_pot import *
from time import sleep
import time
import pandas as pd

SLEEP_TIME = 1

def fix_suggested_price(row):
    suggested_price = row['suggested_price']
    if 'Doppler' in row['market_hash_name'] or 'Marble' in row['market_hash_name']:
        suggested_price = ((row['min_price_sb'] + row['min_price']) / 2) * 1.25

    return suggested_price


def sb_sp_merge(row, df_sb):
    try:
        name_sp, condition_sp = row['market_hash_name'].split(' (')
        condition_sp = condition_sp.replace(')', '').upper().replace(' ', '_').replace('-','_')

        return df_sb[   (df_sb['name'] == name_sp) & 
                        (df_sb['exterior'] == condition_sp) & 
                        (df_sb['statTrak'] == False) & 
                        (df_sb['souvenir'] == False)
                    ]['lowestPrice'].to_list()[0]
    except (IndexError, ValueError) as e:
        return row['min_price']


def define_profit(row):
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



async def get_current_skin_data(api_key, dc_channel, sent_msg, df_sb, accepted_items, eor_string, acceptable_discount, steam_conn):
    # Update Skinport Data
    print('fetching data...')
    start_time = time.time()
    single_search = False
    df_sp = pd.DataFrame.from_records(sp_get_marketplace_items())
    df_sb_old = df_sb
    df_sb = pd.DataFrame.from_records(get_marketplace_list(api_key)['map'])
    df_diff_sb = pd.concat([df_sb, df_sb_old]).drop_duplicates(keep=False)

    if len(df_diff_sb) == 0:
        single_search = True
    else:
        df_sp['min_price_sb'] = df_sp.apply(lambda x: sb_sp_merge(x, df_sb), axis = 1)

    if not single_search:
        print('Using DFs')
        df_below70perc = df_sp[(df_sp['min_price']/df_sp['suggested_price'] < acceptable_discount) | 
                        (df_sp['min_price_sb']/df_sp['suggested_price'] < acceptable_discount)]
    else:
        print('Using single search')
        df_below70perc = df_sp

    df_below70perc_filtered = df_below70perc[df_below70perc['market_hash_name'].isin(accepted_items)].reset_index(drop=True)
    df_below70perc_filtered = df_below70perc_filtered[df_below70perc_filtered['min_price'].notna()]
    if not single_search:
        df_below70perc_filtered = df_below70perc_filtered[df_below70perc_filtered['min_price_sb'].notna()]
        #df_below70perc_filtered['sell_price'] = df_below70perc_filtered.apply(lambda x: define_profit(x), axis = 1)

    # Filter for accepted items and get skinbaron data
    old_sent_msg = sent_msg.copy()
    for i, item in df_below70perc_filtered.iterrows():
        msg = ''
        name_query, name_condition = item['market_hash_name'].replace('★ ', '').split(' (')
        name_condition = name_condition.replace(')', '')
        skinbaron_data = str(get_marketplace_items(name_query, api_key)).replace('},', '},\n')
        formatted_skinbaron_data = format_skinbaron_data(skinbaron_data, name_condition)
        id_nr, name_sb, min_price_sb, mean_price_sb, \
            max_price_sb, quantity_sb, item_page_sb = formatted_skinbaron_data
        min_price_sb = float(min_price_sb)
        item_page_sb = item_page_sb.replace("'", '')

        if not single_search:
            min_price_sb_db = item['min_price_sb']
        else:
            min_price_sb_db = None

        skins_data = [item['market_hash_name'], item['suggested_price'], item['min_price'], 
                float(min_price_sb), min_price_sb_db, item_page_sb,  item['item_page'], id_nr]
        msg, steam_conn, item_and_price = find_profit_items(skins_data, acceptable_discount, steam_conn)

        if msg != '' and item_and_price not in sent_msg:
            sent_msg.append(item_and_price)
            print('Offer found. ApeBot doing ape things.')
            await dc_channel.send(msg)
    
    if old_sent_msg != sent_msg:
        await dc_channel.send(eor_string)
    print(time.time()- start_time)

    return sent_msg, df_sb, steam_conn


if __name__ == '__main__':
    f = open("credentials.json")
    data = json.load(f)
    print(get_current_skin_data(data['skinbaron_api_credentials']['api_key']))


    
