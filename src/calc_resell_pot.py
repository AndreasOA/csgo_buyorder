from src.constants import *

def calc_resell_pot(marketplace: str, buy_price: float, min_price: float, steam_price: float) -> list:
    tier_border = SP_TIER_BORDER if marketplace == 'sp' else SB_TIER_BORDER
    low_tier_fee = SP_SELL_FEE_LOW_TIER if marketplace == 'sp' else SB_SELL_FEE_LOW_TIER
    high_tier_fee = SP_SELL_FEE_HIGH_TIER if marketplace == 'sp' else SB_SELL_FEE_HIGH_TIER

    if marketplace == 'sb':
        buy_price *= (1 + SB_BUY_FEE_SOFORT)

    if min_price <= tier_border:
        sell_price = min_price * (1 - low_tier_fee)
    else:
        sell_price = min_price * (1 - high_tier_fee)

    strat_sell_price = steam_price * (1 - ST_SELL_FEE) * (1 - BUFF_SELL_FEE) * (1 - SP_SELL_FEE_HIGH_TIER) * SELL_BUFFER

    return buy_price, sell_price, strat_sell_price

    



