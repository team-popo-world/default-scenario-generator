from fastapi import APIRouter
from utils.make_graph import make_df_graph1, make_df_graph2_1, make_df_graph2_2, make_df_graph2_3, make_df_graph3, make_df_graph4

router = APIRouter(prefix="/api/graph")

@router.get("/graph1/all")
def graph1_all(userId :str):
    df = make_df_graph1(userId, filter=False)
    file_path = "data/graph1_all.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph1/week")
def graph1_week(userId :str):
    df = make_df_graph1(userId, filter=True)
    file_path = "data/graph1_week.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph2/1/all")
def graph2_1_all(userId :str):
    df = make_df_graph2_1(userId, filter=False)
    file_path = "data/graph2_1_all.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph2/1/week")
def graph2_1_week(userId :str):
    df = make_df_graph2_1(userId, filter=True)
    file_path = "data/graph2_1_week.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph2/2/all")
def graph2_2_all(userId :str):
    df = make_df_graph2_2(userId, filter=False)
    file_path = "data/graph2_2_all.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph2/2/week")
def graph2_2_week(userId :str):
    df = make_df_graph2_2(userId, filter=True)
    file_path = "data/graph2_2_week.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph2/3/all")
def graph2_3_all(userId :str):
    df = make_df_graph2_3(userId, filter=False)
    file_path = "data/graph2_3_all.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph2/3/week")
def graph2_3_week(userId :str):
    df = make_df_graph2_3(userId, filter=True)    
    file_path = "data/graph2_3_week.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph3/all")
def graph3_all(userId :str):
    df = make_df_graph3(userId, filter=False)
    file_path = "data/graph3_all.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph3/week")
def graph3_week(userId :str):
    df = make_df_graph3(userId, filter=True)
    file_path = "data/graph3_week.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph4/all")
def graph4_all(userId :str):
    df = make_df_graph4(userId, filter=False)
    file_path = "data/graph4_all.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")

@router.get("/graph4/week")
def graph4_week(userId :str):
    df = make_df_graph4(userId, filter=True)
    file_path = "data/graph4_week.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ 저장 완료: {file_path}")
    return df.to_dict(orient="records")