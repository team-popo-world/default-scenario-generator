from fastapi import APIRouter
from invest.utils.make_graph import make_df_graph1, make_df_graph2_1, make_df_graph2_2, make_df_graph2_3, make_df_graph3, make_df_graph4
from invest.db.mongo_update import update_mongo_data

router = APIRouter(prefix="/api/graph")

@router.get("/graph1/all")
def graph1_all(userId :str):
    df = make_df_graph1(userId, filter=False)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph1_all_history")
    return json

@router.get("/graph1/week")
def graph1_week(userId :str):
    df = make_df_graph1(userId, filter=True)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph1_week_history")
    return json

@router.get("/graph2/1/all")
def graph2_1_all(userId :str):
    df = make_df_graph2_1(userId, filter=False)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph2_1_all_history")
    return json

@router.get("/graph2/1/week")
def graph2_1_week(userId :str):
    df = make_df_graph2_1(userId, filter=True)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph2_1_week_history")
    return json

@router.get("/graph2/2/all")
def graph2_2_all(userId :str):
    df = make_df_graph2_2(userId, filter=False)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph2_2_all_history")
    return json

@router.get("/graph2/2/week")
def graph2_2_week(userId :str):
    df = make_df_graph2_2(userId, filter=True)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph2_2_week_history")
    return json

@router.get("/graph2/3/all")
def graph2_3_all(userId :str):
    df = make_df_graph2_3(userId, filter=False)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph2_3_all_history")
    return json

@router.get("/graph2/3/week")
def graph2_3_week(userId :str):
    df = make_df_graph2_3(userId, filter=True)    
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph2_3_week_history")
    return json

@router.get("/graph3/all")
def graph3_all(userId :str):
    df = make_df_graph3(userId, filter=False)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph3_all_history")
    return json

@router.get("/graph3/week")
def graph3_week(userId :str):
    df = make_df_graph3(userId, filter=True)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph3_week_history")
    return json

@router.get("/graph4/all")
def graph4_all(userId :str):
    df = make_df_graph4(userId, filter=False)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph4_all_history")
    return json

@router.get("/graph4/week")
def graph4_week(userId :str):
    df = make_df_graph4(userId, filter=True)
    json = df.to_dict(orient="records")
    update_mongo_data(user_id=userId, json_data=json, collection_name="graph4_week_history")
    return json