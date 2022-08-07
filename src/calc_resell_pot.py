SB_SELL_FEE_LOW_TIER = 0.15
SB_SELL_FEE_HIGH_TIER = 0.02
SB_TIER_BORDER = 1300
SB_BUY_FEE_SOFORT = 0.05
BUFF_SELL_FEE = 0.025
SP_TIER_BORDER = 1000
SP_SELL_FEE_LOW_TIER = 0.12
SP_SELL_FEE_HIGH_TIER = 0.06
SP_BUY_FEES = 0.00


def calc_resell_pot(marketplace: str, buy_price: float, min_price: float) -> list:
    tier_border = SP_TIER_BORDER if marketplace == 'sp' else SB_TIER_BORDER
    low_tier_fee = SP_SELL_FEE_LOW_TIER if marketplace == 'sp' else SB_SELL_FEE_LOW_TIER
    high_tier_fee = SP_SELL_FEE_HIGH_TIER if marketplace == 'sp' else SB_SELL_FEE_HIGH_TIER

    if marketplace == 'sb':
        buy_price *= (1 + SB_BUY_FEE_SOFORT)

    if min_price <= tier_border:
        sell_price = min_price * (1 - low_tier_fee)
    else:
        sell_price = min_price * (1 - high_tier_fee)

    sell_price_bf = min_price * (1 - BUFF_SELL_FEE)

    return sell_price

    



