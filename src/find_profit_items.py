import re
import pandas as pd
import numpy as np
from calc_resell_pot import *

SUGGESTED_PRICE_OVER_MIN_PERC = 1.3
ACCEPTABLE_DISCOUNT = 0.70
GOOD_RESELL_DISCOUNT = 0.60


def find_profit_items(skins_data: list) -> list:
    name, suggested_price, min_price_sp, \
    min_price_sb, min_price_sb_db, \
    link_sb, link_sp, sb_id = skins_data
    sb_offer = False
    sp_offer = False
    if min_price_sb_db and min_price_sb_db < min_price_sb:
        link_sb = '**PRICE MISMATCH CHECK MANUAL**\n' + link_sb
        min_price_sb = min_price_sb_db    

    if min_price_sb == 0.0:
        min_price_market = min_price_sp
        sp_offer = True
    elif min_price_sp == 0.0:
        min_price_market = min_price_sb
        sb_offer = True
    elif min_price_sb < min_price_sp:
        min_price_market = min_price_sb
        sb_offer = True
    else:
        min_price_market = min_price_sp
        sp_offer = True

    msg = ''

    if min_price_market < suggested_price * ACCEPTABLE_DISCOUNT:
        sell_price = calc_resell_pot('sb' if sb_offer else 'sp', 
                                      min_price_market, 
                                      min_price_sp if sb_offer else min_price_sb
                                    )
        resell_profit_guar = sell_price - min_price_market
        if resell_profit_guar > 0:
            resell_msg = f'**RESELL WITH EST. PROFIT OF: {resell_profit_guar}**\n'
        else:
            resell_msg = '**NO PROFIT ON INSTA RESELL**\n'
        if sb_offer:
            if resell_profit_guar > 1.00 and min_price_market < 50.00:
                pass
            msg +=  '**SKINBARON** Deal: ' + name + '\n' + \
                    resell_msg + \
                    'Suggested Price: ' + str(suggested_price) + \
                    '€\nBuy Price: ' + str(min_price_market) + \
                    '€\nLowest Skinport Price: ' + str(min_price_sp) + \
                    '€\nSell Price Skinport: ' + str(sell_price) + \
                    '€\nLink Skinbaron: ' + link_sb + \
                    '\nLink Skinport: ' +  link_sp
        elif sp_offer:
            msg +=  '**SKINPORT** Deal: ' + name + '\n' + \
                    resell_msg + \
                    'Suggested Price: ' + str(suggested_price) + \
                    '€\nBuy Price: ' + str(min_price_market) + \
                    '€\nLowest Skinbaron Price: ' + str(min_price_sb) + \
                    '€\nSell Price Skinbaron: ' + str(sell_price) + \
                    '€\nLink Skinport: ' + link_sp + \
                    '\nLink Skinbaron: ' + link_sb

    return msg


if __name__ == '__main__':
    print(find_profit_items({}))
    
