import json

class Constans:
    def __init__(self, telegram_api_token, telegram_chat_id, phone_number, acceptable_discount, good_resell_discount) -> None:
        self.TELEGRAM_API_TOKEN = telegram_api_token
        self.TELEGRAM_CHAT_ID = telegram_chat_id
        self.PHONE = phone_number
        # File for all constant values used
        ####################################################
        # Conv values for symbols in item name for link
        self.SPACE_SYMBOL = '%20'
        self.SPLITTER_SYMBOL = '%7C'
        self.LEFT_BRACKET_SYMBOL = '%28'
        self.RIGHT_BRACKET_SYMBOL = '%29'
        #####################################################
        # Discount values, currently replaced with args
        self.ACCEPTABLE_DISCOUNT = acceptable_discount
        self.GOOD_RESELL_DISCOUNT = good_resell_discount
        #####################################################
        # Fees of different marketplaces
        self.SB_SELL_FEE_LOW_TIER = 0.15
        self.SB_SELL_FEE_HIGH_TIER = 0.02
        self.SB_TIER_BORDER = 1300
        self.SB_BUY_FEE_SOFORT = 0.05
        self.BUFF_SELL_FEE = 0.025
        self.SP_TIER_BORDER = 1000
        self.SP_SELL_FEE_LOW_TIER = 0.12
        self.SP_SELL_FEE_HIGH_TIER = 0.06
        self.SP_BUY_FEES = 0.00
        self.ST_SELL_FEE = 0.131
        self.SELL_BUFFER = 0.95
        #####################################################
        # Misc
        self.SLEEP_TIME = 1
        self.URL = f"https://api.telegram.org/bot{telegram_api_token}/sendMessage?chat_id={telegram_chat_id}&text="

    def getTelegramURL(self):
        return self.URL

    def getSymbolValues(self):
        return self.SPACE_SYMBOL, self.SPLITTER_SYMBOL, \
               self.LEFT_BRACKET_SYMBOL, self.RIGHT_BRACKET_SYMBOL

    def getBuyingConditions(self):
        return self.ACCEPTABLE_DISCOUNT, self.GOOD_RESELL_DISCOUNT

    def getSkinbaronMarketFees(self):
        return self.SB_SELL_FEE_LOW_TIER, self.SB_SELL_FEE_HIGH_TIER, self.SB_BUY_FEE_SOFORT

    def getSkinportMarketFees(self):
        return self.SP_SELL_FEE_LOW_TIER, self.SP_SELL_FEE_HIGH_TIER

    def getBuffMarketFees(self):
        return self.BUFF_SELL_FEE
