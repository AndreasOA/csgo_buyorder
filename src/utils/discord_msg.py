def getDiscordMsg(skins_data: dict):
    if skins_data['profit_sb'] > 0 or skins_data['profit_sp'] > 0 or skins_data['profit_st'] > 0:
        resell_msg = f'**RESELL {round(skins_data["discount"],2)*100}%**\n'
    else:
        resell_msg = f'**NO PROFIT {round(skins_data["discount"],2)*100}%**\n'
    
    return  f"**{skins_data['marketplace']}** Deal: {skins_data['item_name']}\n" + \
            resell_msg + \
            f"Profit SB/SP/ST: {round(skins_data['profit_sb'], 2)}€ / {round(skins_data['profit_sp'], 2)}€ / {round(skins_data['profit_st'], 2)}€\n" + \
            f"Buy SB/SP/ST: {round(skins_data['min_price_sb'], 2)}€ / {round(skins_data['min_price_sp'], 2)}€ / {round(skins_data['min_price_st'], 2)}€\n" + \
            f"Sell SB/SP/ST: {round(skins_data['sell_price_sb'], 2)}€ / {round(skins_data['sell_price_sp'], 2)}€ / {round(skins_data['sell_price_st'], 2)}€\n" + \
            f"Link Skinbaron: {skins_data['link_sb']}\n" + \
            f"Link Skinport: {skins_data['link_sp']}\n" + \
            f"Link Steam: {skins_data['link_st']}"