from fastapi import APIRouter
from invest.utils.make_graph import make_sell_ratio, make_avg_cash_ratio, make_avg_stay_time, make_bet_ratio, make_buy_ratio, make_buy_sell_ratio
from invest.routers.graph import avg_stay_time_all

# one_all = avg_stay_time_all("237aac1b-4d6f-4ca9-9e4f-30719ea5967d") # success
# two_one_all = graph2_1_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_two_all = graph2_2_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_three_all = graph2_3_all("237aac1b-4d6f-4ca9-9e4f-30719ea5967d") # ...(later)
# three = graph3_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# four = graph4_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success