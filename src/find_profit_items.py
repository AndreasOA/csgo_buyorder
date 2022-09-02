from src.discord_msg import *
from src.calc_resell_pot import *
from src.marketplaces.steam import getMarketItemReq
from src.constants import *

def find_profit_items(skins_data: list, acceptable_discount: float, steam_conn: bool) -> list:
    name, suggested_price, min_price_sp, \
    min_price_sb, min_price_sb_db, \
    link_sb, link_sp, sb_id = skins_data
    skins_data_dict = {}
    buy_price = 0.0
    skins_data_dict['item_name'] = name
    skins_data_dict['min_price_st'] = 0
    skins_data_dict['min_price_sp'] = 0
    skins_data_dict['min_price_sb'] = 0
    skins_data_dict['profit_st'] = 0.0
    skins_data_dict['link_st'] = 0
    skins_data_dict['sell_price_st'] = 0.0
    skins_data_dict['sell_price_sp'] = 0.0
    skins_data_dict['sell_price_sb'] = 0.0

    sb_offer = False
    sp_offer = False
    
    
    if min_price_sb_db and min_price_sb_db < min_price_sb:
        skins_data_dict['item_name'] = '**PRICE MISMATCH**   ' + name
        min_price_sb = min_price_sb_db    

    if min_price_sb == 0.0 or min_price_sp == 0.0:
        return '', steam_conn, ''
    elif min_price_sb < min_price_sp:
        min_price_market = min_price_sb
        sb_offer = True
        skins_data_dict['marketplace'] = 'SKINBARON'
        skins_data_dict['profit_sb'] = 0.0
        skins_data_dict['profit_sp'] = 0.0
        skins_data_dict['sell_price_sb'] = 0.0
    else:
        min_price_market = min_price_sp
        sp_offer = True
        skins_data_dict['marketplace'] = 'SKINPORT'
        skins_data_dict['profit_sp'] = 0.0
        skins_data_dict['profit_sb'] = 0.0
        skins_data_dict['sell_price_sp'] = 0.0

    skins_data_dict['discount'] = min_price_market / suggested_price
    skins_data_dict['link_sb'] = link_sb
    skins_data_dict['link_sp'] = link_sp

    if min_price_market < suggested_price * acceptable_discount:
        min_price_st, link_st, steam_conn = getMarketItemReq(name, steam_conn)
        skins_data_dict['link_st'] = link_st
        
        buy_price, sell_price, strat_sell_price = calc_resell_pot('sb' if sb_offer else 'sp', 
                                      min_price_market, 
                                      min_price_sp if sb_offer else min_price_sb,
                                      min_price_st)
        
        skins_data_dict['min_price_st'] = min_price_st
        profit_st = strat_sell_price - buy_price
        profit_sp = sell_price - buy_price
        profit_sb = sell_price - buy_price

        if sb_offer:
            if profit_st > 1.00 and min_price_market < 50.00:
                # implement autobuy here
                pass
            skins_data_dict['min_price_sb'] = buy_price
            skins_data_dict['min_price_sp'] = min_price_sp
            skins_data_dict['profit_sp'] = profit_sp
            skins_data_dict['sell_price_sp'] = sell_price
        elif sp_offer:
            skins_data_dict['profit_sb'] = profit_sb
            skins_data_dict['sell_price_sb'] = sell_price
            skins_data_dict['min_price_sp'] = buy_price
            skins_data_dict['min_price_sb'] = min_price_sb

        skins_data_dict['profit_st'] = profit_st
        skins_data_dict['sell_price_st'] = strat_sell_price

        return getDiscordMsg(skins_data_dict), steam_conn, name + str(buy_price)
    
    else:
        return '', steam_conn, ''


if __name__ == '__main__':
    print(find_profit_items({}))
    
