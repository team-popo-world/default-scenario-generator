from fastapi import APIRouter
from invest.utils.make_graph import make_df_graph1, make_df_graph2_1, make_df_graph2_2, make_df_graph2_3, make_df_graph3, make_df_graph4
from routers.graph import graph1_all, graph1_week, graph2_1_all, graph2_1_week, graph2_2_all, graph2_2_week, graph2_3_all, graph2_3_week, graph3_all, graph3_week, graph4_all, graph4_week

# one_all = graph1_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_one_all = graph2_1_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_two_all = graph2_2_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# two_three_all = graph2_3_all("237aac1b-4d6f-4ca9-9e4f-30719ea5967d") # ...(later)
# three = graph3_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success
# four = graph4_all("956f51a8-d6a0-4a12-a22b-9da3cdffc879") # success