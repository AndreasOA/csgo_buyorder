def getDiscordMsg(skins_data: dict):
    if skins_data['profit_sb'] > 0 or skins_data['profit_sp'] > 0 or skins_data['profit_st'] > 0:
        resell_msg = f'**RESELL**\n'
    else:
        resell_msg = f'**NO PROFIT**\n'
        
    return  f"**{skins_data['marketplace']}** Deal: {skins_data['item_name']}\n" + \
            resell_msg + \
            f"Profit SB/SP/ST: {skins_data['profit_sb']}€ / {skins_data['profit_sp']}€ / {skins_data['profit_st']}€\n" + \
            f"Buy SB/SP/ST: {skins_data['min_price_sb']}€ / {skins_data['min_price_sp']}€ / {skins_data['min_price_st']}€\n" + \
            f"Sell SB/SP/ST: {skins_data['sell_price_sb']}€ / {skins_data['sell_price_sp']}€ / {skins_data['sell_price_st']}€\n" + \
            f"Link Skinbaron: {skins_data['link_sb']}\n" + \
            f"Link Skinport: {skins_data['link_sp']}\n" + \
            f"Link Steam: {skins_data['link_s']}"