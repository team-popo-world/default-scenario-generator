from fastapi import APIRouter
from invest.utils.make_graph import make_sell_ratio, make_avg_cash_ratio, make_avg_stay_time, make_bet_ratio, make_buy_ratio, make_buy_sell_ratio
from invest.routers.graph import avg_stay_time_all, bet_ratio_all, bet_ratio_week

# one_all = avg_stay_time_all("237aac1b-4d6f-4ca9-9e4f-30719ea5967d") # success
# two_one_all = graph2_1_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_two_all = graph2_2_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_three_all = graph2_3_all("237aac1b-4d6f-4ca9-9e4f-30719ea5967d") # ...(later)
# three = graph3_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# four = graph4_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success

# one = make_bet_ratio("fa975c93-78ec-49c6-b60f-e70435f18c34", filter=False)
# print(one)
# two = bet_ratio_week("fa975c93-78ec-49c6-b60f-e70435f18c34")
# print(two)
three = bet_ratio_all("fa975c93-78ec-49c6-b60f-e70435f18c34")
print(three)
# four = make_bet_ratio("fa975c93-78ec-49c6-b60f-e70435f18c34", filter=False)
# print(four)

