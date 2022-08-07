def msg_content(skins_data):
    marketplace = skins_data[0]
    item_name = skins_data[1]
    resell_message = skins_data[2]
    suggested_price = skins_data[3]
    min_price = skins_data[4]
    min_price_om = skins_data[5]
    sell_price = skins_data[6]
    item_page = skins_data[7]
    item_page_om = skins_data[8]

    return  '**' + marketplace + '** Deal: ' + item_name + '\n' + \
        resell_message + \
        'Suggested Price: ' + str(suggested_price) + \
        '€\nBuy Price: ' + str(min_price) + \
        '€\nLowest Skinbaron Price: ' + str(min_price_om) + \
        '€\nSell Price Skinbaron: ' + str(sell_price) + \
        '€\nLink: ' + item_page + \
        '\nLink Skinbaron: ' + item_page_om